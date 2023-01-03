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

db.repository_count.drop()

df_repositories = pd.DataFrame(db.repositories.find())

df_repositories_grouped = df_repositories.groupby([pd.Grouper('classification')]).count()
df_repositories_grouped = df_repositories_grouped.reset_index(level=0)
df_repositories_grouped.rename(columns={"url": "Total Repositories", "classification": "chain"})

print(df_repositories_grouped)

for index, repository_sum in df_repositories_grouped.iterrows():

    print(repository_sum)
    print(repository_sum['url'])
    db.repository_count.insert_one({'Total Repositories': repository_sum['url'], 'chain': repository_sum['classification']}) 
    
