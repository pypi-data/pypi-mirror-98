import pymongo
from bson.objectid import ObjectId
import numpy as np
import pandas as pd
import sys
import os
DATABASE = "auto_ft"

class DBHelper:

    def __init__(self,clear=False):
        if "DB_PORT_27017_TCP_ADDR" in os.environ:
            HOSTIP = os.environ["DB_PORT_27017_TCP_ADDR"]
        else:
            HOSTIP = "localhost"
        self.client = pymongo.MongoClient(HOSTIP, 27017)
        #client = pymongo.MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)
        if clear:
            self.client.drop_database(DATABASE)
        self.db = self.client[DATABASE]

    def add_params(self,config_name,schema_name,bucket_name,folder_name,path,files,cols_lst):
        return self.db.params.insert_one({'config_name':config_name,\
                        'schema_name':schema_name,'bucket_name':bucket_name,'folder_name':folder_name,\
                        'path':path,'files':files,'cols_lst':cols_lst})

    def get_params(self,name):
        return list(self.db.params.find().sort('_id',-1))[0][name]


    def add_file_name(self,file_name):
        return self.db.files.insert_one({'file':file_name})

    def get_file_name(self):
        return list(self.db.files.find().sort('_id',-1))[0]['file']

    def add_entities(self,entity,idx,time_idx,cutoff,if_target,alias):
        return self.db.entities.insert_one({'entity':entity,"idx":idx,"time_idx":time_idx,"cutoff":cutoff,"if_target":if_target,"alias":alias})

    def update_entities(self,df,frn_key):
        target = list(self.db.entities.find({'entity':df}))[-1]
        return self.db.entities.update_one(target, {"$set": {"frn_key":frn_key}})
    def delete_entities(self,table_id):
        self.db.entities.remove({"_id": ObjectId(table_id)})

    def get_entities(self):
        return list(set([e['entity'] for e in self.db.entities.find({},{'_id':0,'entity':1})]))

    def add_relations(self,data_one,data_many,foreign_key):
        return self.db.relations.insert_one({'one':data_one,'many':data_many,'foreign_key':foreign_key})

    def update_relations(self,frn_key):
        target = list(self.db.relations.find().sort('_id',-1))[0]
        return self.db.relations.update_one(target, {"$set": {"frn_key":frn_key}})
    def delete_relations(self,table_id):
        self.db.relations.remove({"_id": ObjectId(table_id)})

    def create_primitive(self,collection_name,df):
        db_table = self.db[collection_name]
        db_table.insert_many(df.to_dict('records'))

    def create_copy(self,collection_name):
        db_tgt=self.db[collection_name+'_cp']
        for c in self.db[collection_name].find():
            db_tgt.insert_one(c)

    def reset_from_cp(self,collection_names):
        for name in collection_names:
            if name+'_cp' in self.db.list_collection_names():
                self.drop_table(name)
                db_tgt=self.db[name]
                for c in self.db[name+'_cp'].find():
                    db_tgt.insert_one(c)

    def update_primitive(self,collection_name,idx,col_name,edit_val):
        col_name_backup=col_name+'_backup'
        edit_val = edit_val.split(',')
        edit_val = [val for val in edit_val if val]

        db_table = self.db[collection_name]
        cur_val = list(db_table.find({'features':idx},{'_id':0,col_name:1}))[0][col_name]
        cur_val_backup = list(db_table.find({'features':idx},{'_id':0,col_name_backup:1}))[0][col_name_backup]
        added = set(edit_val)-set(cur_val)
        rm = set(cur_val)-set(edit_val)
        edit_cur_val_backup = list((set(cur_val_backup)|rm) - added)

        # update value
        db_table.update_one({'features':idx}, {"$set": {col_name:edit_val}})
        db_table.update_one({'features':idx}, {"$set": {col_name_backup:edit_cur_val_backup}})
        return edit_cur_val_backup

    def add_pivotings(self,entity,column1,column2=[],reference=[],ref_type=[]):
        if not column2:
            return self.db.pivotings.insert_one({'entity':entity,'kind':'one','column1':column1,'reference':reference,'ref_type':ref_type})
        return self.db.pivotings.insert_one({'entity':entity,'kind':'two','column1':column1,'column2':column2,'reference':reference,'ref_type':ref_type})
    def delete_pivotings(self,table_id):
        self.db.pivotings.remove({"_id": ObjectId(table_id)})


    def add_features(self,features_init):
        for ft in features_init:
            self.db.features.insert_one({'features':ft})

    def delete_features(self,table_id):
        self.db.features.remove({"_id": ObjectId(table_id)})

    def delete_with_id(self,table_id,collection_name):
        self.db[collection_name].remove({"_id": ObjectId(table_id)})

    def add_ft_restore(self,table_id,collection_from,collection_to):
        ft=list(self.db[collection_from].find({"_id": ObjectId(table_id)},{"_id":0}))[0]['features']
        self.db[collection_to].insert_one({'_id': ObjectId(table_id),'features':ft})

    def delete_ft_restore(self,table_id):
        self.db.ft_restore.remove({"_id": ObjectId(table_id)})

    def get_params(self):
        return list(self.db.params.find().sort('_id',-1))[0]

    def add_updates(self,id_val,gr_val):
        return self.db.updates.insert_one({'id_val':id_val,'gr_val':gr_val})

    def get_updates(self):
        return list(self.db.updates.find())

    def get_col_map(self,file_name,col1,col2):
        col_used = list(self.db[file_name].find({},{'_id':0,col1: 1,col2:1 }))
        col_map = pd.DataFrame(col_used).set_index(col1).T.to_dict('records')
        return col_map[0]

    def add_table(self,file_name,df):
        #if file_name in self.db.list_collection_names():
        #    print('has already')
        #    return
        if file_name in self.db.list_collection_names():
            self.drop_table(file_name)
        db_table = self.db[file_name]
        #db_table_res = self.db[file_name+"_res"]
        params = self.get_params()
        # get the data with smaller size then save into DB to decrease further I/O time
        df = self.helper_agg(df,list([params['ft']]+[params['gr_ft']]),params['cnt_ft'],params['avg_ft'])
        #df_res = self.helper_agg(df,params['gr_ft'],params['cnt_ft']+['cnt'],params['avg_ft'],True)
        #print('df before insert',df)

        db_table.insert_many(df.to_dict('records'))

        # do a backup in order to reset
        if not file_name+'_record_ori' in self.db.list_collection_names():
            db_ori = self.db[file_name+'_record_ori']
            #db_cal = self.db[file_name+'_record_cal']
            #db_col = self.db[file_name+'_cols']
            db_ori.insert_many(df.to_dict('records'))
            #db_cal.insert_many(df_cal.to_dict('records'))
            #db_col.insert_one({'all_used_cols':all_used_cols,'res_used_cols':res_used_cols})
        #db_table_res.insert_many(df_res.to_dict('records'))

    def update_table(self,file_name,ft_val,gr_ft_val):
        db_table = self.db[file_name]
        #db_res = self.db[file_name+"_res"]
        params = self.get_params()

        '''
        #extract old values
        myquery = {params["ft"]:ft_val}
        find_doc = list(db_table.find(myquery))[0]
        ori_grp, ori_cnt_val, ori_avg_val = find_doc[params['gr_ft']],\
                                                [find_doc[f] for f in params['cnt_ft']],\
                                                [find_doc[f] for f in params['avg_ft']]
        '''
        #update new values
        db_table.update_one({params["ft"]: ft_val}, {"$set": {params["gr_ft"]:gr_ft_val}})

    def get_table_one(self,file_name):
        return list(self.db[file_name].find_one())

    def get_final(self,file_name):
        df_ori,df_res,_,_=self.get_table(file_name)
        return df_res,df_ori

    def get_table(self,file_name,withid=True):
        if withid:
            return list(self.db[file_name].find().sort("_id"))
        else:
            return list(self.db[file_name].find({},{'_id':0}))


    def get_defalt(self,file_name):
        # drop current updated collection
        if file_name+'_record_ori' in self.db.list_collection_names():
            self.drop_table(file_name)
            # get the presaved default table
            db_ori = self.db[file_name+'_record_ori']
            df_ori = pd.DataFrame(db_ori.find())
            # write into the file_name collection
            db_table = self.db[file_name]
            db_table.insert_many(df_ori.to_dict('records'))
        else:
            return


    def drop_table(self,file_name):
        if file_name in self.db.list_collection_names():
            self.db[file_name].drop()

    def helper_cal(self,df,cnt_ft,avg_ft,round_n=2):
        #df[cnt_ft]=df[cnt].apply(lambda x:x/df['cnt'])
        for f in cnt_ft:
            df[f+'_count']=df[f].apply(len)
            df.drop(columns=f,inplace=True)
        for ft in avg_ft:
            df[ft+'_rate']=(df[ft]/df['cnt']).round(round_n)
            df.drop(columns=ft,inplace=True)

        df.drop(columns='cnt',inplace=True)
        return df

    def helper_agg(self,df,g_col,cnt_col,rate_col,if_res=False):#,round_n=2):
        def m(col):
            return list(set(sum(col,[])))
        if if_res: #for the result table
            cal_cnt = {cnt:lambda x:m(x) for cnt in cnt_col}
        else: #for the original table
            cal_cnt = {cnt:lambda x:list(set(x)) for cnt in cnt_col}

        cal_rt = {rt:np.sum for rt in rate_col}
        cal_all = {**cal_cnt,**cal_rt}
        df_out = df.groupby(g_col).agg(cal_all)#.round(round_n)
        if not if_res:
            all_cnts = df.groupby(g_col).size()
            all_cnts.name = 'cnt'
            df_out = df_out.join(all_cnts)
        df_out=df_out.reset_index()
        df_out.drop_duplicates(subset=g_col,inplace=True)
        return df_out

    def helper_rename(self,df,dedup_col):
        df.columns = ["_".join(x) for x in df.columns.ravel()]
        df.reset_index(inplace=True)
        #ensure no duplicates in the index
        df.drop_duplicates(subset=dedup_col,inplace=True)
        return df
