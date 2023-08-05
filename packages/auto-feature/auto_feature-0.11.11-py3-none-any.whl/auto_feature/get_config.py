from dbhelper import DBHelper
from collections import defaultdict
from smart_open import open as s_open
import os
import pickle
import boto3
import json
from get_ft_features import prepare_config
from helper import COL_PLACEHOLDER

DB = DBHelper()

def get_default(collections:list,agg_tfm:str):
    # prms are the colletions for primitives
    # ag_tfm is the field name for agg and transform
    prm_map = defaultdict(set)
    default = set()
    for name in collections:
        tfms = list(DB.db[name].find({},{'_id':0,'type':1,agg_tfm:1}))
        #print(tfms)
        if not agg_tfm in tfms[0]:
            #print('{} not in'.format(agg_tfm))
            continue
        for t in tfms:
            #print(t)
            prm_map[t['type']]|=set(t[agg_tfm])
            default|=set(t[agg_tfm])

    return list(default),prm_map


def get_prm_option(prms:list,agg_tfm:str,agg_tfm_map:dict,agg_prm_default:list):
    p_options = {}
    for name in prms:
        alias = list(DB.db.entities.find({'entity':name},{'_id':0,'alias':1}))[0]['alias']
        tfms = list(DB.db[name].find({},{'_id':0,'type':1,'features':1,agg_tfm:1}))

        if not agg_tfm in tfms[0]:
            #print('{} not in'.format(agg_tfm))
            continue

        for t in tfms:
            cur_primitives = set(t[agg_tfm])
            map_primitives = agg_tfm_map[t['type']]
            if t['type']=='pivot':
                map_primitives = set(agg_prm_default.copy())
            difs = map_primitives-cur_primitives
            if difs:
                for dif in difs:
                #dif = tuple(dif) if len(dif)>1 else list(dif)[0]
                    primitives = p_options.get(dif,{})
                    inside = primitives.get('ignore_variables',{})
                    inside[alias]=list(set(inside.get(alias,[])+[t['features']]))
                    primitives['ignore_variables']=inside
                    p_options[dif]=primitives
    return p_options



def get_configure(path,config_name):
    all_collections=DB.db.list_collection_names()
    config = {}

    # get entities, relations, and pivotings

    entities = DB.get_table('entities',withid=False)
    relations = DB.get_table('relations',withid=False)
    pivotings = DB.get_table('pivotings',withid=False)


    config['entities']=entities
    config['relations']=relations
    config['pivotings']=pivotings

    ## get primitives

    collections = [c for c in all_collections if c not in ['entities','pivotings','relations','features','ft_restore']]
    #collections = [c for c in collections if not c.endswith('_cp')]



    # get default transform and agg primitives and the map
    tfm_prm_default,tfm_prm_map=get_default(collections,'tfm_prm')
    agg_prm_default,agg_prm_map = get_default(collections,'agg_prm')

    ''' ##map is like below
    ##agg_prm_map is like:
    ##defaultdict(set,
                {'index': {'count'},
                 'int64': set(),
                 'object': {'mode', 'num_unique'},
                 'pivot': {'count', 'if_exist'}})
    '''


    config['pmt_agg_kpt']= agg_prm_default
    config['pmt_tfm_kpt']= tfm_prm_default
    config['where_primitives'] = list(agg_prm_map['pivot'])

    # get primitive options

    ''' ## primitive options is like below; we mainly use ignore_variables
    primitive_options={
         'mode': {'include_variables': {'log': ['product_id', 'zipcode'],
                                       'sessions': ['device_type'],
                                         'customers': ['cancel_reason']}},
         'weekday': {'ignore_variables': {'customers':
                                              ['signup_date',
                                                'cancel_date']}}})
    '''


    primitive_options={}
    primitive_options_agg=get_prm_option(collections,'agg_prm',agg_prm_map,agg_prm_default)
    primitive_options_agg_combo = {tuple([k for k in primitive_options_agg.keys() if primitive_options_agg[k] == v]): v for v in list(primitive_options_agg.values())}

    primitive_options_tfm=get_prm_option(collections,'tfm_prm',tfm_prm_map,tfm_prm_default)
    primitive_options_tfm_combo = {tuple([k for k in primitive_options_tfm.keys() if primitive_options_tfm[k] == v]): v for v in list(primitive_options_tfm.values())}

    primitive_options = {**primitive_options_agg_combo,**primitive_options_tfm_combo}

    config['primitive_options']=primitive_options

    # tease out all the talbes will be used
    config['all_data']=[entity['entity'] for entity in config['entities']]+[p['reference'] for p in config['pivotings'] if p['reference']!=COL_PLACEHOLDER[0]]
    #new_config = prepare_config(config)
    print('cinfig_name',config_name)
    with s_open(os.path.join(path,'{}.pickle'.format(config_name)), 'wb') as handle:
        pickle.dump(config, handle)
