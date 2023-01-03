import pandas as pd
import pymongo
from pandas import DataFrame
import streamlit as st
import numpy as np
import datetime
from datetime import timedelta


 #==========Get Data=============
 
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

