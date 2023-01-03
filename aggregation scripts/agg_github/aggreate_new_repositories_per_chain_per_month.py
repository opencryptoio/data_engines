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

db.new_repositories_per_mo.drop()

df_repositories = pd.DataFrame(db.repositories.find({'created_at': {'$exists': True }}))

df_repositories['created_at'] = pd.to_datetime(df_repositories['created_at'])

df_month = df_repositories.groupby([pd.Grouper(key='created_at', axis=0, freq='M'), pd.Grouper('classification')]).count()

for index, element in df_month.iterrows():

    db.new_repositories_per_mo.insert_one({'chain': element.name[1], 'date': element.name[0], 'total_repositories': int(element["url"])})

