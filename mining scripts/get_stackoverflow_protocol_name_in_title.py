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
mongo_client = pymongo.MongoClient({"ATLAS_URI=mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority"})
db = mongo_client["Crypto01"]

#get protocol names
"""
query_date = datetime.today() - timedelta(days=0)
coin_query = {'repository_scrape_date': {'$lt': str(query_date.isoformat())}}
all_coins = db.chains.find(coin_query).sort('chainId', -1)


#initialte variables from toml file
data = toml.load("key_words.toml")
primary_crypto_terms = data["primary_crypto_terms"]
secondary_crypto_terms = data["secondary_crypto_terms"]
coins_with_unique_names = data["coins_with_unique_names"]
coins_with_unique_names = [coin_name.lower() for coin_name in coins_with_unique_names]

"""

#delte previous mongo db collection
#db.stackoverflow_question_sums.drop()

#iteration through protocols

import requests

stillpages = True
offset = 0

while stillpages:

    url = "https://api.footprint.network/api/v1/protocol/list?limit=5&offset=" + offset

    headers = {
        "accept": "application/json",
        "API-KEY": "BSRwU/mgc0sfUEHFavqJRRfHfBaIEes41kzaZQpvRTz/PYtHz/7QptspxkXriV8N"
    }

    response = requests.get(url, headers=headers)
    json_response = json.loads(response.text)


    try:
        if json_response["items"] == []:
                break    
    except:
            break

    for element in json_response["data"]:
            
            try:
                db.stackoverflow_question_sums.insert_one({'chain': coin["coin"], 'question_counter':int(question_counter)})
                

print(response.text)


for coin in all_coins:

    week = 0
    duplicate_counter = 0

    #if not coin['coin'] == "Polygon":
        #continue

    page = 1
    question_counter = 0
    unique_name_coin = coin["coin"].lower() in coins_with_unique_names

    #infite loop to iterate through query pages
    while True:
        
        time.sleep(5)   

        #query string passed on with the protocol name and page as params
        url = "https://api.stackexchange.com/2.3/search/advanced?page=" + str(page) + "&pagesize=100&order=desc&sort=activity&title=" + coin["coin"] + "&site=stackoverflow"
        
        page += 1

        params = {'key':{"key"}}
   
        response = requests.request("GET", url, params=params)

        json_response = json.loads(response.text)
        print(json_response)
        
        #loop until respone items are empty
        try:
            if json_response["items"] == []:
                break    
        except:
            break

        #iterate through response items
        for element in json_response["items"]:
            
            first_term_match = False
            found = False
            
            try:
                
                #pass on stackoverflow question title to var
                if element["title"] is not None:
                    element_title = element["title"].lower()
                else: element_title = ""
                
            
                #key word rules to filter out false positive items.
                
                #Rule 1: if crypto name unique such as Ethereum, Polkadot, zkSync etc.
                if unique_name_coin:
                    found = True
                
                #Rule 2: iterating through primary keywords and checking if they are in the question title
                if not found:
                    for term in primary_crypto_terms:
                        if term in element_title or unique_name_coin:
                            found = True
                            break
                
                #Rule 3: iterating through secondary keywords and checking if they are in the question title.                 
                if not found:
                    for term in secondary_crypto_terms:
                        if term in element_title and first_term_match == False:
                            first_term_match = True
                            continue
                        if term in element_title and first_term_match == True:
                            found = True
                            break
                    
                        
                if found:

                    question_counter += 1
            
                    
            except Exception as e:
                print(e)
                print ('type is:', e.__class__.__name__)
                print_exc()
                pass


    print(coin["coin"] + "/" + str(question_counter))
    #db.stackoverflow_question_sums.insert_one({'chain': coin["coin"], 'question_counter':int(question_counter)})
    

        












