from queue import Empty
import requests
import json
import pymongo
import time
from pymongo.errors import DuplicateKeyError
import pandas as pd
from datetime import datetime
from traceback import print_exc

#connect to db
mongo_client = pymongo.MongoClient({"mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority"})
db = mongo_client["Crypto01"]

db.protocols_per_chain.drop()
db.protocols_per_chain.create_index("protocol_slug") #"protocol_type", "protocol_name"

offset = 0

while True:

    url = "https://api.footprint.network/api/v1/protocol/list?limit=2000&offset=" + str(offset)

    headers = {
        "accept": "application/json",
        "API-KEY": "BSRwU/mgc0sfUEHFavqJRRfHfBaIEes41kzaZQpvRTz/PYtHz/7QptspxkXriV8N"
    }

    response = requests.get(url, headers=headers)
    json_response = json.loads(response.text)

    try:
        if json_response["data"] == []:
                break    
    except:
            break

    time.sleep(2)

    db.protocols_per_chain.insert_many(json_response["data"])

    offset += 2000

    print("added")
    print(json_response["data"])












    """

    for element in json_response["data"]:
            
            try:
                db.protocols_per_chain.insert_one({ "protocol_slug": element["protocol_slug"],
                                                    "chain": element["chain"],
                                                    "protocol_type": element["protocol_type"],
                                                    "protocol_sub_type": element["protocol_sub_type"],
                                                    "protocol_name": element["protocol_name"],
                                                    "logo": element["logo"],
                                                    "discord": element["discord"],
                                                    "github": element["github"],
                                                    "twitter": element["twitter"],
                                                    "telegram": element["telegram"],
                                                    "web_url": element["web_url"],
                                                    "description": element["description"],
                                                    "created_at": element["created_at"],
                                                    "created_by": element["created_by"],
                                                    "updated_at": element["updated_at"]
                                                   })

                print("added" + element["protocol_slug"])

                offset+=2000

            
            except Exception as e:
                print(e)
                print("failed" + element["protocol_slug"])
                pass

        """
            