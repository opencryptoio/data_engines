import pandas as pd
import pymongo
from pandas import DataFrame
import streamlit as st
import numpy as np
import datetime
from datetime import timedelta





 #==========Get Data=============
 
senior_dev_cut_off = datetime.datetime.now() - timedelta(days=3*365)
 
mongo_client = pymongo.MongoClient("mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority")

db = mongo_client["Crypto01"]

all_repositories = list(db.repositories.find())
all_commits = list(db.commits.find())

senior_dev_cut_off = datetime.datetime.now() - timedelta(days=3*365)
all_senior_developers = list(db.developer.find({'first_commit': {'$lt': str(senior_dev_cut_off.isoformat())}}))

df_merged_repositories_commits = pd.merge(DataFrame(all_repositories), DataFrame(all_commits), left_on=['url'], right_on=['repository'], how='inner')
df_merged_repositories_commits_developers = pd.merge(DataFrame(df_merged_repositories_commits), DataFrame(all_senior_developers), left_on=['developer'], right_on=['name'], how='inner')

df_data_senior_devs = df_merged_repositories_commits_developers
df_data_senior_devs['commit_date']= pd.to_datetime(df_data_senior_devs['commit_date'])


db.commits_per_chain_sen_dev_1w.drop()

df_week = df_data_senior_devs.groupby([pd.Grouper(key='commit_date', axis=0, freq='1W'), pd.Grouper('classification')]).count()

for index, element in df_week.iterrows():
    
    print(element.name[0])
    print(element.name[1])
    print(element["url_x"])
    
    db.commits_per_chain_sen_dev_1w.insert_one({'chain': element.name[1], 'date': element.name[0], 'commits': int(element["url_x"])})
    
    
db.commits_per_chain_sen_dev_1m.drop()
    
df_month = df_data_senior_devs.groupby([pd.Grouper(key='commit_date', axis=0, freq='M'), pd.Grouper('classification')]).count()

for index, element in df_month.iterrows():
    
    print(element.name[0])
    print(element.name[1])
    print(element["url_x"])
    
    db.commits_per_chain_sen_dev_1m.insert_one({'chain': element.name[1], 'date': element.name[0], 'commits': int(element["url_x"])})


              