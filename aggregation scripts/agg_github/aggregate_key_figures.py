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

db.totals.drop()

df_repositories_count = pd.DataFrame(db.repositories.find())
df_developers_count = pd.DataFrame(db.developer.find())
#df_commits_count = pd.DataFrame(db.commits.find())

db.totals.insert_one({'Total Repositories': df_repositories_count.shape[0], 'Total Developers': df_developers_count.shape[0]}) 



    