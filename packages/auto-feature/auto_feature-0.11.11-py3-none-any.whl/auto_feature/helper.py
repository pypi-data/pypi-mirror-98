import json
import boto3
import pandas as pd
import os
import io

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top

COL_PLACEHOLDER = ["Don't have"]

DEFAULT_SELECT = "Select Entity First"
csvfolderpath = os.path.join(APP_ROOT, 'OutputFolder')

# prmitives
agg_prm=\
{'object':['num_unique','mode'],
'int64':['sum','max','min','mean'],
'float64':['sum','max','min','mean'],
'datetime64[ns]':[],
'bool':['max_bol','sum_bol',],
'index':['count'],
'time_index':['time_since_first','time_since_last','avg_time_between'],
'pivot':['count','if_exist']
}


tfm_prm=\
{'object':[],
'int64':[],
'float64':[],
'datetime64[ns]':['week_day','is_weekend','seasons','partofday'],
'bool':[],
'index':[],
'time_index':['week_day','is_weekend','seasons','partofday'],
'pivot':[]
}

backup_agg_prm=\
{'object':['first','last','entropy'],
'int64':['std','skew','trend','median'],
'float64':['std','skew','trend','median'],
'datetime64[ns]':['min_time','max_time'],
'bool':['any','all','percent_true'],
'index':[],
'time_index':['min_time','max_time'],
'pivot':['time_since_first','time_since_last']}

backup_tfm_prm=\
{'object':['first','last','entropy'],
'int64':['cum_min','cum_max','percentile'],
'float64':['cum_min','cum_max','percentile'],
'datetime64[ns]':['second','minute','hour','day','month','year'],
'bool':[],
'index':[],
'time_index':['time_since_previous','second','minute','hour','day','month','year'],
'pivot':[]
}
# s3 dataset
'''
with open('path.json',"r") as f:
    configs= json.load(f)
config_name = configs['config_name']
bucket_name = configs['bucket_name']
pre = configs['prefix']
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
path = os.path.join('s3://',bucket_name,pre)
'''
def pd_read(file_name,bucket_name,pre,src='s3',sample=None,used_cols=None):
    if src=='test':
        csvFile = os.path.join(csvfolderpath, file_name)
    else:
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
