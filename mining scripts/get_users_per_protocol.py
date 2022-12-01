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
import toml

#connect to db
mongo_client = pymongo.MongoClient({"mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority"})
db = mongo_client["Crypto01"]

#get protocol names

db.users_per_protocol.drop()
db.users_per_protocol.create_index("protocol_slug") #"protocol_type", "protocol_name"

all_protocols = pd.DataFrame(db.protocols_per_chain.find().limit(1000))

all_protocols = all_protocols["protocol_slug"].unique()

print(len(all_protocols))

for protocol in all_protocols:

    offset = 0

    while True:

        url = "https://api.footprint.network/api/v1/protocol/" + protocol + "/daily_stats?limit=2000&offset=" + str(offset)

        headers = {
            "accept": "application/json",
            "API-KEY": "BSRwU/mgc0sfUEHFavqJRRfHfBaIEes41kzaZQpvRTz/PYtHz/7QptspxkXriV8N"
        }

        #BSRwU/mgc0sfUEHFavqJRRfHfBaIEes41kzaZQpvRTz/PYtHz/7QptspxkXriV8N
        #ASDhKGLedgMHHjN9m1PQQB7hFSDoGt2vBvfxjOLBTpHDkmab1OTznH0vjEHfbjZM

        offset+=2000

        response = requests.get(url, headers=headers)
        json_response = json.loads(response.text)

        print(json_response)

        try:
            if json_response["data"] == []:
                    break    
        except:
                break

        time.sleep(2)

        db.users_per_protocol.insert_many(json_response["data"])

        print("iteration")

        """

        for element in json_response["data"]:
                
                try:
                    db.users_per_protocol.insert_one({
                                                        "on_date": element["on_date"],
                                                        "chain": element["chain"],
                                                        "protocol_slug": element["protocol_slug"],
                                                        "protocol_name": element["protocol_name"],
                                                        "number_of_active_users": element["number_of_active_users"],
                                                        "number_of_new_users": element["number_of_new_users"],
                                                        "number_of_total_users": element["number_of_new_users"],
                                                        "new_users_1d_pct_change": element["new_users_1d_pct_change"],
                                                        "new_users_7d_pct_change": element["new_users_7d_pct_change"],
                                                        "new_users_30d_pct_change": element["new_users_30d_pct_change"],
                                                        "new_users_180d_pct_change": element["new_users_180d_pct_change"],
                                                        "new_users_360d_pct_change": element["new_users_360d_pct_change"],
                                                        "active_users_1d_pct_change": element["active_users_1d_pct_change"],
                                                        "active_users_7d_pct_change": element["active_users_7d_pct_change"],
                                                        "active_users_30d_pct_change": element["active_users_30d_pct_change"],
                                                        "active_users_180d_pct_change": element["active_users_180d_pct_change"],
                                                        "active_users_360d_pct_change": element["active_users_360d_pct_change"]
                                                    })
                    print("added" + element["protocol_slug"])

                    

                except Exception as e:
                    print(e)
                    print("failed" + element["protocol_slug"])
                    pass
                    

            """

