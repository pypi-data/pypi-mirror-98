import os
import pkg_resources
import sys
#from config import configs
#import argparse
#import click
import json
'''
def change_config(bkt,pre,out):
    my_file = pkg_resources.resource_filename('auto_feature', 'path.json')
    #my_file = 'path.json'
    #print('file in cli is:',my_file)
    with open(my_file,"r") as f:
        data = json.load(f)
    data['bucket_name']=bkt
    data['prefix']=pre if pre[-1]=='/' else pre+'/'
    data['output_name']=out if out.endswith('.csv') or out.endswith('.xlsx') or out.endswith('.parquet') else out+'.csv'
    with open(my_file, 'w') as outfile:
        json.dump(data, outfile)
'''
#@click.command()
#@click.option('-b', '--bucket',prompt="bucket name",default='va-vdas-workspace-prod')
#@click.option('-p', '--prefix',prompt="path after bucket",default='<i-number>/<project>')
#@click.option('-o', '--output',prompt="output name with extension",default='out.csv')
def main():
    #change_config(bucket,prefix,output)
    #print('path in cli main is,',os.getcwd())
    os.chdir(os.path.join(pkg_resources.get_distribution("auto_feature").location,"auto_feature"))
    os.system('bash run_docker.sh')# --build')

if __name__=='__main__':
    main()
