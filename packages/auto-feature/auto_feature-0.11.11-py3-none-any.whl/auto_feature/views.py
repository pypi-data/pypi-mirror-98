# to do list: 1.add infer schema function (df.infer_object().dtype)
#             2. make one datasets have more than one frn keys (need to consider DB's update_entities)
#             3. can't edit when the cell is empty (primitives)
#             4. add time_unit option
#             5. add groupby primitive (for transformatin like time_since_previous)
#             6. primitive_cp might be removed
#             7. time_unit ; cutoff
#             8. data type how to convert pandas datatype into featuretools.
#             9. sample (then need to make all the unique values selected in the intr values; then within ft_agg, do the samping, not from read data!)
# notes: cols not drop after concat can simply use set(frn)+set(idx)-set(time_index) (leave time index)
# notes: all the check, for "columns2" check, use if column2 in xxx; for 'reference'or'time_idx', use 'reference'==COL_PLACEHOLDER[0]
from flask import Flask,render_template,request,redirect,url_for,jsonify,make_response,jsonify,session
from flask_wtf import FlaskForm
from wtforms import SelectField,TextField,SubmitField,SelectMultipleField,widgets
from wtforms.validators import URL, DataRequired
import pandas as pd
import os
from itertools import product
import pyarrow as pa
import pyarrow.parquet as pq
from dbhelper import DBHelper
import json
import datetime
import numpy as np
import sys
import boto3
import s3fs
import io
import xlsxwriter
from get_config import get_configure
from get_ft_features import get_features,save_ft
from helper import *
#from grouping import app


import urllib.request
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SECRET_KEY']='0212'
DB = DBHelper(clear=True)

url = "http://randomfactgenerator.net"
#bucket_name = ""
#config_name = ""
#folder_name = ""
#path = ""
#files =[]
#cols_lst = {}



# s3 dataset
#with open('path.json',"r") as f:
#    configs= json.load(f)
#config_name = configs['config_name']
#bucket_name = configs['bucket_name']
#pre = configs['prefix']
#s3 = boto3.resource('s3')
#bucket = s3.Bucket(bucket_name)
#path = os.path.join('s3://',bucket_name,pre)




# define form class
class Select2MultipleField(SelectMultipleField):
    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""

class path_form(FlaskForm):
    bucket =   TextField('Bucket', [DataRequired(),])
    #folder =    SelectField('Folder',choices=[])
    folder =    TextField('Folder',[DataRequired(),])
    configuration=  TextField('Configuration', [DataRequired(),])
    schema_name=  TextField('Schema_name', [DataRequired(),])

class entity_form(FlaskForm):
    entity = SelectField('Entity',choices=[])
    idx = SelectMultipleField('Index',choices=[])
    #choices = MultiCheckboxField('Routes', coerce=int)
    time_idx = SelectField('Time_Index',choices=[])
    cutoff = SelectField('Cutoff',choices=[])
    if_target = SelectField('If_target',choices=COL_PLACEHOLDER+['yes','no'])
    alias = TextField('Alias', [DataRequired(),])
    submit = SubmitField("Submit")

class relations_form(FlaskForm):
    many = SelectField('Many',choices=[])
    one = SelectField('One',choices=[])
    foreign_key = SelectMultipleField('Foreign_Key',choices=[])
    submit = SubmitField("Submit")

class primitives_form(FlaskForm):
    datasets = SelectField('Datasets',choices=[])
    submit = SubmitField("Submit")
    reset = SubmitField("Reset")

class pivoting_form(FlaskForm):
    entity = SelectField('Entity',choices=[])
    column1 = SelectMultipleField('Column1',choices=[])
    column2 = SelectMultipleField('Column2',choices=[])
    reference = SelectField('Reference',choices=[])
    ref_type = SelectField('Ref_type',choices=[])
    submit = SubmitField("Submit")


@app.route('/')
def home():
    if not session.get('logged_in'):
        p_form = path_form()
        return render_template('directory.html',p_form=p_form)
    return render_template('home.html', path=session.get('path'),config_name=session.get('config_name'),\
                                        schema_name = session['schema_name'])

@app.route('/directory', methods=['GET','POST'])
def directory():
    p_form=path_form()
    if request.method=="POST":
        session['config_name'] = p_form.configuration.data
        session['schema_name'] = p_form.schema_name.data
        session['bucket_name'] = p_form.bucket.data
        folder_name= p_form.folder.data
        session['folder_name'] = folder_name if folder_name.endswith('/') else folder_name+'/'
        #print('b and pre',(bucket_name,pre))
        session['path'] = os.path.join('s3://',session['bucket_name'],session['folder_name'])
        session['logged_in'] = True
        session['files'] = get_file_names(session['bucket_name'],session['folder_name'])
    return home()#redirect(url_for('/',p_form=p_form))#home()

'''
@app.route('/directory/<bucket>')
def get_directory(bucket):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)

    result = bucket.meta.client.list_objects(Bucket=bucket.name,Delimiter='/',Prefix=)
    folders = [o.get('Prefix') for o in result.get("CommonPrefixes")]
    return jsonify({"folders":folders})
'''
@app.route('/re_directory')
def re_directory():
    session['logged_in']=False
    return render_template('re_directory.html')


@app.route('/entities',methods=["GET","POST"])
def entities():
    ent_form = entity_form()
    print('session files',session['files'])
    # defaul cols values
    ent_form.idx.choices = [(DEFAULT_SELECT,DEFAULT_SELECT)]
    ent_form.entity.choices = [DEFAULT_SELECT]+[file for file in session['files']]
    ent_form.time_idx.choices = [DEFAULT_SELECT]
    ent_form.cutoff.choices = [DEFAULT_SELECT]

    # get user submit
    if request.method=="POST":
        entity = ent_form.entity.data
        idx = ent_form.idx.data
        alias = ent_form.alias.data
        time_idx = ent_form.time_idx.data
        cutoff = ent_form.cutoff.data
        if_target = ent_form.if_target.data
        DB.add_entities(entity,'|'.join(idx),time_idx,cutoff,if_target,alias)

    tables = DB.get_table('entities')
    return render_template('entities.html', ent_form=ent_form, tables=tables)


@app.route('/col/<entity>')
def col(entity):
    if session.get(entity+'col'):
        print("in session: ",session[entity+'col'])
        cols = session[entity+'col']
    else:
        cols = get_col(entity,src='s3',bucket_name=session['bucket_name'],pre=session['folder_name'])
        session[entity+'col']=cols #as cache, since get_col takes time.
    return jsonify({"cols":cols})

@app.route("/entities/deletetable")
def entities_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_entities(tableid)
    return redirect(url_for('entities'))


@app.route('/relations',methods=['GET','POST'])
def relations():
    entities_in_db = DB.get_entities()
    rel_form = relations_form()

    rel_form.one.choices = [DEFAULT_SELECT]+[file for file in entities_in_db]
    rel_form.many.choices = [DEFAULT_SELECT]+[file for file in entities_in_db]
    rel_form.foreign_key.choices = [(DEFAULT_SELECT,DEFAULT_SELECT)]

    # get user submit
    if request.method=="POST":
        many = rel_form.many.data
        one = rel_form.one.data
        foreign_key = rel_form.foreign_key.data
        DB.add_relations(one,many,'|'.join(foreign_key))
        DB.update_entities(many,'|'.join(foreign_key))
    tables = DB.get_table('relations')
    return render_template('relations.html', rel_form=rel_form, tables=tables)

@app.route("/relations/deletetable")
def relations_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_relations(tableid)
    return redirect(url_for('relations'))
'''
@app.route("/primitives/change")
def primitives_change():
    entities_in_db = DB.get_entities()
    df_name = request.args.get("file_name")
    if df_name in DB.db.list_collection_names():
        df_types = pd.DataFrame(DB.get_table(df_name,False))
    else:
        df = pd_read(df_name,src='s3')
        df_types = get_primitive_infer(df,df_name)
        DB.create_primitive(df_name,df_types)

    ajax_df = json.dumps(df_types.to_dict('records'))
    all_used_cols = df_types.columns.tolist()
    all_used_cols = json.dumps(all_used_cols)

    idx_col = 'features'
    edit_col = ['tfm_prm','agg_prm']
    return redirect(url_for('primitives', files =entities_in_db, all_used_cols=all_used_cols,\
    ajax_df=ajax_df,file_name = df_name,indx=idx_col,edit_col=json.dumps(edit_col)))
'''

# havn't created the copy
@app.route('/primitives',methods=['GET','POST'])
def primitives():
    prim_form = primitives_form()
    entities_in_db = DB.get_entities()
    prim_form.datasets.choices = [file for file in entities_in_db]

    df_name = entities_in_db[0] #default values
    # get user submit
    if request.method=="POST":
        df_name = prim_form.datasets.data
#    entities_in_db = DB.get_entities()

#    check if df_name already exist, then no need to calcuate the type again
    if df_name in DB.db.list_collection_names():
        df_types = pd.DataFrame(DB.get_table(df_name,False))
    else:
        df = pd_read(df_name,bucket_name=session['bucket_name'],pre =session['folder_name'], src='s3')
        df_types = get_primitive_infer(df,df_name)
        DB.create_primitive(df_name,df_types) #no need to create copy since we are using the saved javascrip variable to do reset
        #DB.create_copy(df_name)

    ajax_df = json.dumps(df_types.to_dict('records'))
    #ajax_df_res = json.dumps(data_res.to_dict('records'))
    #res_df = data_res.to_html(index = False)
    all_used_cols = df_types.columns.tolist()
    all_used_cols = json.dumps(all_used_cols)
    #res_used_cols = json.dumps(res_used_cols)
    idx_col = 'features'
    edit_col = ['tfm_prm','agg_prm']
    return render_template('primitives.html', prim_form=prim_form, all_used_cols=all_used_cols,\
    ajax_df=ajax_df,file_name = df_name,indx=idx_col,edit_col=json.dumps(edit_col))


@app.route('/update', methods=["POST"])
def update():
    #file_name = DB.get_file_name()''
    data = request.get_data()
    data = json.loads(data)
    #return jsonify(dict(redirect='display'))

    edit_cur_val_backup = do_update(data)
    return jsonify({'edit_cur_val_backup': edit_cur_val_backup})

@app.route('/reset')
def reset():
    # using the javascrip variabel to reset
    return "reset"


@app.route('/pivotings',methods=["GET","POST"])
def pivotings():
    pvt_form = pivoting_form()
    entities_in_db = DB.get_entities()
    pvt_form.entity.choices = [DEFAULT_SELECT]+[file for file in entities_in_db]
    pvt_form.column1.choices = [(DEFAULT_SELECT,DEFAULT_SELECT)]
    pvt_form.column2.choices = [(DEFAULT_SELECT,DEFAULT_SELECT)]
    pvt_form.reference.choices = COL_PLACEHOLDER+[file for file in session['files']]
    pvt_form.ref_type.choices = COL_PLACEHOLDER+['range','map']

    # get user submit
    if request.method=="POST":
        entity = pvt_form.entity.data
        column1 = pvt_form.column1.data
        column2 = pvt_form.column2.data
        reference = pvt_form.reference.data
        ref_type = pvt_form.ref_type.data

        if isinstance(column2,list):
            DB.add_pivotings(entity,'|'.join(column1),'|'.join(column2),reference,ref_type)
        else:
            DB.add_pivotings(entity,'|'.join(column1),reference,ref_type)

    tables = DB.get_table('pivotings')
    return render_template('pivotings.html', pvt_form=pvt_form, tables=tables)

@app.route("/pivotings/deletetable")
def pivotings_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_pivotings(tableid)
    return redirect(url_for('pivotings'))

@app.route("/remove/<string:collection>")
def remove_collection(collection):

    if collection=='primitives':
        entities_in_db = DB.get_entities()
        for ent in entities_in_db:
            DB.drop_table(ent)
    else:
        DB.drop_table(collection)
    return '{} is removed from database'.format(collection)


@app.route("/remove/all")
def remove_all():
    #remove primitives
    DB.client.drop_database('auto_ft')
    return 'the database is removed'

@app.route('/save')
def save():
    get_configure(session['path'],session['config_name'])
    return render_template("save.html",config_name=session['config_name'],path=session['path'])

@app.route('/save_wait')
def save_wait():
    content = urllib.request.urlopen(url).read()
    parsedHTML = BeautifulSoup(content)
    tag = parsedHTML.find_all('div',{'id':'z'})[0]
    fact = re.search('<div id="z">(.+?)<br/>',str(tag))
    fact = fact.group(1)
    return render_template('save_wait.html',fact=fact)

@app.route('/save_schema')
def save_schema():
    ft_rm = [f['features'] for f in DB.get_table('ft_restore',withid=False)]
    #ft_features = session['ft_features']
    save_ft(ft_rm,session['path'],session['schema_name'])
    return render_template("save_schema.html",schema_name=session['schema_name'],path=session['path'])

@app.route('/save_schema_wait')
def save_schema_wait():
    content = urllib.request.urlopen(url).read()
    parsedHTML = BeautifulSoup(content)
    tag = parsedHTML.find_all('div',{'id':'z'})[0]
    fact = re.search('<div id="z">(.+?)<br/>',str(tag))
    fact = fact.group(1)
    return render_template('save_schema_wait.html',fact=fact)


@app.route('/preview',methods=["GET","POST"])
def preview():
    #prv_form = preview_form()
    tables = DB.get_table('features')
    tables_rm = DB.get_table('ft_restore')
    return render_template('preview.html', tables=tables, tables_rm=tables_rm)#prv_form=prv_form, )

@app.route("/preview/create")
def preview_create():
    print('path and config',(session['path'],session['config_name']))
    DB.drop_table('features')
    DB.drop_table('ft_restore')

    features_init = get_features(session['bucket_name'],session['folder_name'],session['config_name'],session['schema_name'])#,session['featuretools_ft']
    DB.add_features(features_init)
    return redirect(url_for('preview'))

@app.route('/preview_wait')
def preview_wait():
    content = urllib.request.urlopen(url).read()
    parsedHTML = BeautifulSoup(content)
    tag = parsedHTML.find_all('div',{'id':'z'})[0]
    fact = re.search('<div id="z">(.+?)<br/>',str(tag))
    fact = fact.group(1)
    return render_template('preview_wait.html',fact=fact)

@app.route("/preview/deletetable")
def preview_deletetable():
    tableid = request.args.get("tableid")
    DB.add_ft_restore(tableid,'features','ft_restore')
    DB.delete_features(tableid)

    return redirect(url_for('preview'))

@app.route("/preview/restore")
def preview_restore():
    tableid = request.args.get("tableid")
    DB.add_ft_restore(tableid,'ft_restore','features')
    DB.delete_ft_restore(tableid)
    return redirect(url_for('preview'))

def get_file_names(bucket_name,pre):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    print('bucket and pre in s3 in get_file_name',(bucket_name,pre))

    s3_file_names = []
    for obj in bucket.objects.filter(Delimiter='/',Prefix=pre):
        f = obj.key.split('/')[-1]
        if f:
            s3_file_names.append(f)
    print('files in s3 in get_file_name',s3_file_names)
    files = [file for file in s3_file_names if file.endswith(".csv") or file.endswith(".parquet")\
                                                or file.endswith(".xlsx")]
    return files

def do_update(data):
    #data = json.loads(data)
    idx,edit_val,col_name,df_name = data['row_id'],data['edit'],data['col'],data['df_name']
    edit_cur_val_backup=DB.update_primitive(df_name,idx,col_name,edit_val)
    edit_cur_val_backup = json.dumps(edit_cur_val_backup)
    return edit_cur_val_backup


def get_primitive_infer(df,df_name):
    is_target=False
    # get pivoting features
    if 'pivotings' in DB.db.list_collection_names():
        is_pivot=True
        pivot_cols = list(DB.db.pivotings.find({'entity':df_name},{'_id':0,'column1':1,'column2':1}))
        pvt_cols = []
        '''
        for p_c in pivot_cols:
            p = list(p_c.values())
            pvt_cols+=[c.split('|') for c in p]
        pvt_cols=list(set(sum(pvt_cols,[])))
        '''
        for p_c in pivot_cols:
            if 'column2' in p_c:
                p=[x[0]+'_'+x[1] for x in list(product(p_c['column1'].split('|'),p_c['column2'].split('|')))]
            else:
                p = list(p_c.values())
                p=[c.split('|') for c in p]
            pvt_cols+=p
    #if DB.
    df_type = df.dtypes.astype(str)
    info = list(DB.db.entities.find({'entity':df_name}))[-1]
    # deal with index

    if info['idx']!=COL_PLACEHOLDER[0]:
        for c in info['idx'].split('|'):
            df_type[c]='index'
    if 'frn_key' in info:
        for c in info['frn_key'].split('|'):
            df_type[c]='index'
    else:
        is_target=True
    if info['time_idx'] !=COL_PLACEHOLDER[0]:
        df_type[info['time_idx']]='time_index'

    # deal with pivoting
    for c in pvt_cols:
        df_type[c]='pivot'

    df_types = pd.DataFrame(df_type,columns=['type']).reset_index().rename(columns={'index': 'features'})
    if not is_target:
        df_types['agg_prm']=df_types['type'].apply(lambda x:list(set(agg_prm[x])))
        df_types['agg_prm_backup']=df_types['type'].apply(lambda x:list(set(backup_agg_prm[x])))
    df_types['tfm_prm']=df_types['type'].apply(lambda x:list(set(tfm_prm[x])))
    df_types['tfm_prm_backup']=df_types['type'].apply(lambda x:list(set(backup_tfm_prm[x])))

    return df_types

def get_col(file,src='s3',bucket_name=None,pre=None):
    print("in get col")
    if file==DEFAULT_SELECT:
        print('feautre are defualt: ',DEFAULT_SELECT)
        return [DEFAULT_SELECT]
    if src=='test':
        print("features are test: ")
        file_path = os.path.join(csvfolderpath, file)
    else:
        print("features are s3: ")
        file_path = os.path.join("s3://",os.path.join(bucket_name,pre),file)
    #csvFile = os.path.join(csvfolderpath, file)
    if file.endswith('.csv'):
        print('read csv with path',file_path)
        table = pd.read_csv(file_path, nrows=10)
    if file.endswith('.xlsx'):
        print('read xlsx with path',file_path)
        s3_c = boto3.client('s3')
        file_path = os.path.join(pre,file)
        obj = s3_c.get_object(Bucket=bucket_name, Key=file_path)
        data = obj['Body'].read()
        table = pd.read_excel(io.BytesIO(data),nrows=10)
    if file.endswith('.parquet'):
        table = pd.read_parquet(file_path,  engine='pyarrow')
        table = table.head(10)
    cols = COL_PLACEHOLDER+table.columns.tolist()
    return cols

def post_value_with_fallback(key):
    if request.form.get(key):
        return request.form.get(key)
    return DEFAULT_SELECT

def post_values_with_fallback(key):
    if request.form.getlist(key):
        return request.form.getlist(key)
    return DEFAULT_SELECT

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULT_SELECT

def get_values_with_fallback(key):
    if request.args.getlist(key):
        return request.args.getlist(key)
    if request.cookies.getlist(key):
        return request.cookies.getlist(key)
    return DEFAULT_SELECT


'''
@app.route('/', methods=['POST'])
def upload_files():
    for uploaded_file in request.files.getlist('file'):
        filename = uploaded_file.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        #uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))
@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
@app.route('/Login')
def Login():
    return render_template('login.html')
'''
def get_table(user_input):
    dict={user_input:'hi'}
    return dict    #returns list of dictionaries, for example...
                   #dict = [{'name':'Joe','age':'25'},
                  #        {'name':'Mike','age':'20'},
                  #        {'name':'Chris','age':'29'}]


if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0')
