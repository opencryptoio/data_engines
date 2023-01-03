import requests
import json
import pymongo
import time
import datetime
from datetime import datetime, timedelta

mongo_client = pymongo.MongoClient("mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority")

db = mongo_client["Crypto01"]

db.chains.drop()

url = "https://api.llama.fi/chains"

response = requests.request("GET", url)

json_coindata = json.loads(response.text)

for item in json_coindata:
    
    if item['name'] == "Near":
        name = "Near Protocol"
    else: name = item['name']
    
    db.chains.insert_one({'coin': name, 'slug': item['gecko_id'], 'symbol': item['tokenSymbol'], 'chainId': item['chainId'], 'repository_scrape_date': (datetime.today() - timedelta(days=7)).isoformat()})
    

