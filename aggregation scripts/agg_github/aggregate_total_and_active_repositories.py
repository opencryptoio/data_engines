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

print(df_all_commits.shape)

df_merged_commits_repositories = pd.merge(DataFrame(df_all_commits), DataFrame(df_all_repositories), left_on=['repository'], right_on=['url'], how='inner')

print(df_merged_commits_repositories)
print(df_merged_commits_repositories.columns)

#Criteria 1: Filter active repositories. Must have at least 1 commit consecutiely for the last three months. 
#Sum of commits per repository per month
df_merged_commits_repositories.reset_index(inplace=True)
df_merged_commits_repositories['commit_date']= pd.to_datetime(df_merged_commits_repositories['commit_date'])
df_commits_per_rep_per_month = df_merged_commits_repositories.groupby([pd.Grouper(key='commit_date', axis=0, freq='1M'), pd.Grouper('repository')]).count()
df_commits_per_rep_per_month.reset_index(inplace=True)

#Filter repositories who had at least 5 commit per month consecutively consecutively for the last 3 months
start_time = datetime.datetime.now() - timedelta(days=31)
df_active_repos = df_commits_per_rep_per_month.loc[(df_commits_per_rep_per_month['commit_date']>str(start_time)) & (df_commits_per_rep_per_month['index'] > 1)]
df_active_repos.reset_index(inplace=True)
print(df_active_repos)

#Sum total repos per protocol
df_total_repos_per_protocol = df_all_repositories.groupby([pd.Grouper(key='classification')]).count()
df_total_repos_per_protocol.reset_index(inplace=True)

print(df_total_repos_per_protocol)
print(df_total_repos_per_protocol.columns)

#Sum active repos per protocol
df_active_repos_per_protocol = pd.merge(DataFrame(df_active_repos['repository']), DataFrame(df_all_repositories), left_on=['repository'], right_on=['url'], how='left').groupby([pd.Grouper(key='classification')]).count()
df_active_repos_per_protocol.reset_index(inplace=True)

print(df_active_repos_per_protocol)
print(df_active_repos_per_protocol.columns)

db.sum_active_repos_per_protocol.drop()

for index, element in df_total_repos_per_protocol.iterrows():

    print(element["classification"])
    print(element["_id"])

    try:
        active_repositories = df_active_repos_per_protocol.loc[(df_active_repos_per_protocol["classification"]=="Ethereum")].iloc[0]['_id']
    except:
        active_repositories = 0
        
    db.sum_active_repos_per_protocol.insert_one({'protocol': element["classification"], 'total repositories': int(element["_id"]), 'active repositories': int(active_repositories)})


