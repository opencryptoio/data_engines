from queue import Empty
import requests
import json
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


#connect to db
mongo_client = pymongo.MongoClient({"mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority"})
db = mongo_client["Crypto01"]

#get protocol names

db.DT_users_per_protocol.drop()
db.DT_users_per_protocol.create_index("protocol_slug") #"protocol_type", "protocol_name"

all_protocols = pd.DataFrame(db.DT_protocols_per_chain.find({"users_per_protocol_transfer":{"$exists": False}}))

print(all_protocols)

all_protocols = all_protocols["protocol_slug"].unique()

print(len(all_protocols))
counter = 0

for protocol in all_protocols:

    offset = 0
    print(counter)
    counter += 1

    db.protocols_per_chain.update_one({"protocol_slug" : protocol},{"$set":{"users_per_protocol_transfer": True}})

    while True:

        url = "https://api.footprint.network/api/v1/protocol/" + protocol + "/daily_stats?limit=100&offset=" + str(offset)

        headers = {
            "accept": "application/json",
            "API-KEY": "ASDhKGLedgMHHjN9m1PQQB7hFSDoGt2vBvfxjOLBTpHDkmab1OTznH0vjEHfbjZM"
        }

        #BSRwU/mgc0sfUEHFavqJRRfHfBaIEes41kzaZQpvRTz/PYtHz/7QptspxkXriV8N
        #ASDhKGLedgMHHjN9m1PQQB7hFSDoGt2vBvfxjOLBTpHDkmab1OTznH0vjEHfbjZM

        offset+=100

        response = requests.get(url, headers=headers)
        json_response = json.loads(response.text)


        try:
            if json_response["data"] == []:
                    break    
        except:
                break

        time.sleep(0)

        db.DT_users_per_protocol.insert_many(json_response["data"])

        print("iteration")