import pandas as pd, numpy as np
from collections import defaultdict
import os
import pickle
import argparse
import sys
import click
import json
import boto3
import io
import s3fs
from smart_open import open as s_open
import xlsxwriter
from itertools import product
import re
from functools import reduce
import featuretools as ft
from ftools import ft_agg




class read_files():


    def get_files(self):
        # get config
        with s_open(os.path.join('s3://',bucket_name,pre,'config.pickle'), 'rb') as handle:
            config = pickle.load(handle)

        # get datas
        config['datas'] = []
        for file_name in config['input_name']:
            #print('input name is ',file_name)
            data = self.pd_read(file_name)
            config['datas'].append(data)
        return config

    @staticmethod
    def pd_read(file_name,src='s3',sample=None,used_cols=None):
        #print('b,p,file_name',(bucket_name,pre,file_name))
        csvFile = os.path.join('s3://',bucket_name,pre,file_name)
        table=None
        if csvFile.endswith('.csv'):
            table = pd.read_csv(csvFile, nrows=sample,usecols=used_cols)
        if csvFile.endswith('.xlsx'):
            s3_c = boto3.client('s3')
            file_path = os.path.join(pre,file_name)
            obj = s3_c.get_object(Bucket=bucket_name, Key=file_path)
            data = obj['Body'].read()
            table = pd.read_excel(io.BytesIO(data),nrows=sample)

        if csvFile.endswith('.parquet'):
            table = pd.read_parquet(csvFile,engine='pyarrow',columns=used_cols)
            if sample:
                table = table.head(sample)
        return table



class get_interesting_vals():
    def __init__(self,config):
        #this part need to change when there are more grouping datas
        self.config=config
        self.interesting_values = defaultdict(list)
        self.grp_inputs = config['grp_inputs'][0]
        self.grp_features = config['grp_features'][0]
        self.grp_type=config['grp_type'][0]
        self.grp_out=config['grouping'][0]

    def map_grouping(self):
        if self.grp_type=='range':
            grp = read_files.pd_read(self.grp_inputs)
            ft = self.grp_features
            bins = self.create_bin(grp,ft)
            print('bins is',bins)
            self.config['datas'][0][ft]=self.my_cut(ft,self.config['datas'][0][ft],bins,right=True,include_lowest=True)
        else:
            maps = pd.Series(grp[self.grp_out].values,index=grp[self.grp_features]).to_dict()
            self.config['datas'][0].map(maps)

    def get_intr_vals(self):
        if self.config['if_intr_value']:
            for i,fts in enumerate(self.config['itr_fts']):
                if fts:
                    for ft in fts:
                        if ft in self.interesting_values:
                            self.config['itr_vals'][i].append(self.interesting_values[ft])
                        else:
                            self.config['itr_vals'][i].append(self.config['datas'][i][ft].unique().tolist())
        if self.config['if_prod_itr']:
            for i,fts in enumerate(self.config['prod_itr_fts']):
                if fts:
                    for j,ft in enumerate(fts):
                        #print(j,ft)
                        new_ft = '_'.join(ft)
                        self.config['prod_itr_fts'][i][j]=new_ft
                        # generate new product features
                        self.config['datas'][i][new_ft]=self.config['datas'][i][ft[0]].astype(str)+"_"+self.config['datas'][i][ft[1]].astype(str)
                        ft=[self.interesting_values[f] if f in self.interesting_values else self.config['datas'][i][f].unique().tolist() for f in ft]
                        #ft0 = interesting_values[f0] if f0 in interesting_values else config['datas'][i][ft].unique().tolist()
                        itr_val = [x[0]+'_'+x[1] for x in list(product(ft[0],ft[1]))]
                        self.config['prod_itr_vals'][i].append(itr_val)

    def create_bin(self,df,col):
        bins = []
        for val in df[col]:
            if "<=" in val:
                val = int(val.strip("<="))
            elif ">=" in val:
                continue
                #val = int(val.strip(">="))
            else:
                val = int(val.split("-")[-1])
            bins.append(val)
        return bins

    def my_cut(self,col,x, bins,lower_infinite=True, upper_infinite=True,**kwargs):
        """
        Wrapper around pandas cut() to create infinite lower/upper bounds with proper labeling.

        Takes all the same arguments as pandas cut(), plus two more.

        Args :
            lower_infinite (bool, optional) : set whether the lower bound is infinite
                Default is True. If true, and your first bin element is something like 20, the
                first bin label will be '<= 20' (depending on other cut() parameters)
            upper_infinite (bool, optional) : set whether the upper bound is infinite
                Default is True. If true, and your last bin element is something like 20, the
                first bin label will be '> 20' (depending on other cut() parameters)
            **kwargs : any standard pandas cut() labeled parameters

        Returns :
            out : same as pandas cut() return value
            bins : same as pandas cut() return value
        """

        # Quick passthru if no infinite bounds
        if not lower_infinite and not upper_infinite:
            return pd.cut(x, bins, **kwargs)

        # Setup
        num_labels      = len(bins) - 1
        include_lowest  = kwargs.get("include_lowest", False)
        right           = kwargs.get("right", True)

        # Prepend/Append infinities where indiciated
        bins_final = bins.copy()
        if upper_infinite:
            bins_final.insert(len(bins),float("inf"))
            num_labels += 1
        if lower_infinite:
            bins_final.insert(0,float("-inf"))
            num_labels += 1

        # Decide all boundary symbols based on traditional cut() parameters
        symbol_lower  = "<=" if include_lowest and right else "<"
        left_bracket  = "(" if right else "["
        right_bracket = "]" if right else ")"
        symbol_upper  = ">" if right else ">="

        # Inner function reused in multiple clauses for labeling
        def make_label(i, lb=left_bracket, rb=right_bracket):
            return "{0}{1}, {2}{3}".format(lb, bins_final[i], bins_final[i+1], rb)

        # Create custom labels
        labels=[]
        for i in range(0,num_labels):
            new_label = None

            if i == 0:
                if lower_infinite:
                    new_label = "{0} {1}".format(symbol_lower, bins_final[i+1])
                elif include_lowest:
                    new_label = make_label(i, lb="[")
                else:
                    new_label = make_label(i)
            elif upper_infinite and i == (num_labels - 1):
                new_label = "{0} {1}".format(symbol_upper, bins_final[i])
            else:
                new_label = make_label(i)

            labels.append(new_label)
        self.interesting_values[col]=labels
        # Pass thru to pandas cut()
        return pd.cut(x, bins_final, labels=labels, **kwargs)


def feature_engineer():
    # get files and assign to config
    rf = read_files()
    config = rf.get_files()
    print('get files done')

    # get intereting values wiht the grouping files
    giv = get_interesting_vals(config)
    giv.map_grouping()
    giv.get_intr_vals()
    print('get interesting vals ready')

    # feature engineering
    config = giv.config.copy()
    ent = ft_agg(config)
    en_set,cutoff = ent.get_entityset()
    agg_used,tfm_used,whr_pmts = ent.get_prmts()

    if config['process']=='dev':
        features = ent.run_dfs(es=en_set,cutoff=cutoff,featureonly=True)
        features_kep = post_process(features,config,bucket_name,pre)
    else:
        features_kep = config['features']
    print('get feature schema done')
    vin_res = ent.calculate_matrix(en_set,features_kep,cutoff=cutoff)
    vin_reset_idx = ent.recover_col(vin_res,config['keys'][-1],en_set[config['names'][-1]].index)
    print('get output ready')
    vin_reset_idx.to_csv(os.path.join('s3://',bucket_name,pre,output_name))
    print('save successfully')

def post_process(features,config,bucket_name,pre):
    min_ig = r'(SUM|MEAN|MAX)[(|<].*MIN[(|<].*|(MIN|SUM|MEAN)[(|<].*MAX[(|<].*|(MIN|SUM|MEAN)[(|<].*COUNT[(|<].*|(MIN|SUM|MEAN)[(|<].*NUM_UNIQUE[(|<].*|(MIN|SUM|MAX)[(|<].*MEAN[(|<].*|(MEAN|MIN|SUM)[(|<].*SUMBOL[(|<].*|(MEAN|MIN)[(|<].*SUM[(|<].*'
    p_min = re.compile(min_ig)

    features_kep = [f for i,f in enumerate(features) if not p_min.match(f.get_name())]
    features_kep = [f for f in features_kep if not 'frn' in f.get_name()]

    if config['ig_ent_after']:
        for c in config['ig_ent_after']:
            ig_ent = r'{}\..*\(.*'.format(c)
            ent_ig = re.compile(ig_ent)
            features_kep=[f for i,f in enumerate(features_kep) if not ent_ig.match(f.get_name())]

    kys = set(reduce(lambda x,y:x+y,config['keys']))
    kys_not_drp = set(config['keys_not_drp_after'])
    kys_drp = list(kys-kys_not_drp)
    for c in kys_drp:
        features_kep = [f for f in features_kep if not c in f.get_name()]
    if config['add_back']:
        for k,v in config['add_back'].items():
            features_kep += [ft.Feature(en_set[k][v])]

    ft.save_features(features_kep, os.path.join('s3://',bucket_name,pre,"schema.json"))
    print('save schema sucessfully')
    return features_kep

if __name__=='__main__':
    # get s3 path for datas
    #print('run path:',os.getcwd())
    with open('path.json',"r") as f:
        s3_path= json.load(f)
    bucket_name = s3_path['bucket_name']
    pre = s3_path['prefix']
    output_name = s3_path['output_name']
    feature_engineer()
