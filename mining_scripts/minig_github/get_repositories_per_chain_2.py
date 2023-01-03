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

mongo_client = pymongo.MongoClient("mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["Crypto01"]

query_date = datetime.today() - timedelta(days=0)
coin_query = {'repository_scrape_date': {'$lt': str(query_date.isoformat())}}
all_coins = db.chains.find(coin_query).sort('chainId', -1)

primary_crypto_terms = ["cryptocurrency", " crypto ", "blockchain", "binance", "ether", " solidity ", "motoko", "substrate", " defi ", "dapp", " Dapp ", " ico ", " Ico ", " ICO ", "nft", "smart contract", "buterin", "Buterin", "satoshi", "Satoshi"]
secondary_crypto_terms = [" coin ", " token ", " chain ", " ledger ", "wallet ", " node ", "decentralized", "cold storage", " hodl ", "exchange", " mining "]

coins_with_unique_names = ["Optimism", "Ethereum", "Arbitrum", "Arbitrum Nova", "Moonbeam", "Moonriver", "OKExChain", "Solana", "Wanchain", "OntologyEVM", "Velas", "Kucoin", "Milkomeda", "Milkomeda", "Bitcoin", "IoTex", "Kusama", "Polkadot", "Litecoin", "Klaytn", "Zilliqa", "ThunderCore", "Sifchain", "Elastos", "Algorand", "Thorchain", "Karura", "Tezos", "Ravencoin", "Genshiro", "EthereumClassic", "TomoChain", "Cardano", "zkSync", "VeChain", "Godwoken", "Hedera", "Echelon", "Syscoin", "Kujira"]
coins_with_unique_names = [coin_name.lower() for coin_name in coins_with_unique_names]



for coin in all_coins:

    week = 0
    duplicate_counter = 0

    #if not coin['coin'] == "Ethereum":
        #continue

    for weeks in range(500):
        
        query_starting_date = datetime.today() - timedelta(weeks=week)
        string_query_starting_date = f'{query_starting_date:%Y-%m-%d}'
        query_ending_date = (datetime.today() - timedelta(weeks=week - 2))
        string_query_ending_date = f'{query_ending_date:%Y-%m-%d}'
    
        page = 1
        week += 2

        while True:
            
            time.sleep(1)    
            
            url = "https://api.github.com/search/repositories?q=" + coin["coin"] + "+created:" + string_query_starting_date + ".." + string_query_ending_date + "&per_page=100&page=" + str(page)
            
            page += 1
            
            payload={}
            headers = {
                'Authorization': 'token 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'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            json_response = json.loads(response.text)
            
            try:
                if json_response["items"] == []:
                    break    
            except Exception as e:
                break

                
            for element in json_response["items"]:
                
                first_term_match = False
                found = False
                
                try:
                    
                    if element["description"] is not None:
                        element_description = element["description"]
                    else: element_description = ""
                    
                
                    for term in primary_crypto_terms:

                        unique_name_coin = coin["coin"].lower() in coins_with_unique_names
                        name_in_url = coin["coin"].lower() in element["url"].lower()
                        name_in_description = condition3 = coin["coin"].lower() in element_description.lower()

                        if term in element_description.lower() or (unique_name_coin and name_in_url) or (unique_name_coin and name_in_description):
                            found = True
                                
                        
                    if not found:
                        for term in secondary_crypto_terms:
                            if term in element_description.lower() or term in element["url"].lower() and first_term_match == False:
                                first_term_match == True
                                continue
                            if term in element_description.lower() or term in element["url"].lower() and first_term_match == True:
                                found = True
                        
                            
                    if found:
                                                
                        try:
                            
                            duplicate_record = db.repositories.find({
                                        '$and': [
                                            { 'url': element["url"] },
                                            { 'classification': coin["coin"] }
                                        ]
                                        }
                                    )  

                            if pd.DataFrame(duplicate_record).empty:
                                db.repositories.insert_one({'id': element["id"], 'url': element["url"], 'classification': coin["coin"], 'forks': element["forks"], 'issues': element["open_issues_count"] , 'commit_scrape_date': "", 'created_at': element["created_at"]})
                                print("added: " + coin["coin"] + " / " + element["url"])

                            else: 
                                print("dublicate: " + url + " / " + coin["coin"] + " / " + element["url"]) 
                            
                        except Exception as e:
                            print(e)
                            print ('type is:', e.__class__.__name__)
                            print_exc()
                            pass


                    else: print("not added: " + coin["coin"] + " / " + element["url"])
                
                        
                except Exception as e:
                    print(e)
                    print ('type is:', e.__class__.__name__)
                    print_exc()
                    pass
                                                    
    
        db.chains.update_one({'_id': ObjectId(coin["_id"])}, {'$set': {'repository_scrape_date': datetime.today().isoformat()}})
    

        







