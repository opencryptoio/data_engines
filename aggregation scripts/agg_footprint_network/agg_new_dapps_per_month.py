from queue import Empty
import pymongo
import time
from bson.objectid import ObjectId
from datetime import datetime
from traceback import print_exc
from pymongo.errors import DuplicateKeyError
from datetime import timedelta
from collections import Counter
import pandas as pd
from datetime import datetime
import toml

#connect to db
mongo_client = pymongo.MongoClient({"mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority"})
db = mongo_client["Crypto01"]


db.new_dapps_per_month.drop()

df_chains_per_protocol = pd.DataFrame(db.protocols_per_chain.find().limit(300))

df_chains_per_protocol["created_at"] = pd.to_datetime(df_chains_per_protocol['created_at'])

df_count_of_p_per_month = df_chains_per_protocol.groupby((pd.Grouper(key="created_at", freq='1M'))).count()
df_count_of_p_per_month.reset_index()

print(df_count_of_p_per_month)

for index, month in df_count_of_p_per_month.iterrows():

    db.new_dapps_per_month.insert_one({"date": str(index), "count": int(month["protocol_slug"])})


