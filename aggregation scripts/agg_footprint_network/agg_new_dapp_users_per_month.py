from queue import Empty
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from traceback import print_exc
from pymongo.errors import DuplicateKeyError
from datetime import timedelta
import pandas as pd
import toml

#connect to db
mongo_client = pymongo.MongoClient({"mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority"})
db = mongo_client["Crypto01"]

db.new_dapp_users_per_month.drop()

df_users_per_protocol = pd.DataFrame(db.users_per_protocol.find())

df_users_per_protocol["on_date"] = pd.to_datetime(df_users_per_protocol['on_date'])

df_count_of_new_users_per_protocol_per_month = df_users_per_protocol.groupby((pd.Grouper(key="on_date", freq='1M'))).sum()

print(df_count_of_new_users_per_protocol_per_month.columns)

for index, month in df_count_of_new_users_per_protocol_per_month.iterrows():
    db.new_dapp_users_per_month.insert_one({"date": index, "count": int(month["number_of_active_users"])})