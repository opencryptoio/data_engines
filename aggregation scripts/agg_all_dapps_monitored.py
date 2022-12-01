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


# Get dapps type count

#=============================

db.all_dapps_monitored_count.drop()

#df_users_per_protocol = pd.DataFrame(db.users_per_protocol.find())  #{"on_date": { "$eq": "2022-01-24"}}
df_chains_per_protocol = pd.DataFrame(db.protocols_per_chain.find())

df_chains_per_protocol_count = pd.DataFrame(df_chains_per_protocol.groupby("protocol_type").count())
df_chains_per_protocol_count.reset_index()

for index, type in df_chains_per_protocol_count.iterrows():

    db.all_dapps_monitored_count.insert_one({"type": index, "count": int(type["protocol_slug"])})


