import pandas as pd
import pymongo
from pandas import DataFrame
import streamlit as st
import numpy as np
import datetime
from datetime import date, timedelta


 #==========Get Data=============
mongo_client = pymongo.MongoClient("mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["Crypto01"]


df_all_commits = pd.DataFrame(db.commits.find())
df_all_repositories = pd.DataFrame(db.repositories.find())


#Criteria 1: Filter all devs who made first commit more than 2 years ago
senior_dev_cut_off = datetime.datetime.now() - timedelta(days=2*365)
df_all_senior_developers = list(db.developer.find({'first_commit': {'$lt': str(senior_dev_cut_off.isoformat())}}))

print(len(df_all_senior_developers))

#Criteria 2: Filter devs who made last year more than 10 commits
#Sum commits of devs per year
df_all_commits.reset_index(inplace=True)
df_all_commits['commit_date']= pd.to_datetime(df_all_commits['commit_date'])
df_commits_per_dev_per_month = df_all_commits.groupby([pd.Grouper(key='commit_date', axis=0, freq='1M'), pd.Grouper('developer')]).count()
df_commits_per_dev_per_month.reset_index(inplace=True)

#Filter devs who did more than 10 commits in the last 3 months
start_time = datetime.datetime.now() - timedelta(days=120)
df_commits_per_active_developer = df_commits_per_dev_per_month.loc[(df_commits_per_dev_per_month['commit_date']>str(start_time)) & (df_commits_per_dev_per_month['index'] > 1)]
df_commits_per_active_developer.reset_index(inplace=True)
print(df_commits_per_active_developer)

#Merge Filtered Dataframes
df_merged_senior_and_active_developers = pd.merge(DataFrame(df_all_senior_developers), DataFrame(df_commits_per_active_developer), left_on=['name'], right_on=['developer'], how='inner')
print(df_merged_senior_and_active_developers)

#Merge with all commits Dataframe to get all the commits of senior and active developers
df_merged_commits_senior_and_active_developers = pd.merge(DataFrame(df_merged_senior_and_active_developers), DataFrame(df_all_commits), left_on=['name'], right_on=['developer'], how='inner')
df_merged_repos_commits_senior_and_active_developers = pd.merge(DataFrame(df_merged_commits_senior_and_active_developers), DataFrame(df_all_repositories), left_on=['repository_y'], right_on=['url'], how='inner')
df_merged_repos_commits_senior_and_active_developers.reset_index(inplace=True)

print(df_merged_senior_and_active_developers)

db.commits_per_chain_sen_active_dev_1w.drop()

print(df_merged_senior_and_active_developers.columns)

df_week = df_merged_repos_commits_senior_and_active_developers.groupby([pd.Grouper(key='commit_date_y', axis=0, freq='1W'), pd.Grouper('classification')]).count()

for index, element in df_week.iterrows():
    
    print(element.name[0])
    print(element.name[1])
    print(element["url_x"])
    
    db.commits_per_chain_sen_active_dev_1w.insert_one({'chain': element.name[1], 'date': element.name[0], 'commits': int(element["url_x"])})
    
    
db.commits_per_chain_sen_active_dev_1m.drop()

df_week = df_merged_repos_commits_senior_and_active_developers.groupby([pd.Grouper(key='commit_date_y', axis=0, freq='1M'), pd.Grouper('classification')]).count()

for index, element in df_week.iterrows():
    
    print(element.name[0])
    print(element.name[1])
    print(element["url_x"])
    
    db.commits_per_chain_sen_active_dev_1m.insert_one({'chain': element.name[1], 'date': element.name[0], 'commits': int(element["url_x"])})

              