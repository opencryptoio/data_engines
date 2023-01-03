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
all_coins = db.chains.find(coin_query).sort('chainId', 1)

primary_crypto_terms = ["cryptocurrency", " crypto ", "blockchain", "binance", "ether", " solidity ", "motoko","substrate", " defi ", "dapp", " Dapp ", " ico ", " Ico ", " ICO ", "nft", "smart contract", "buterin", "Buterin", "satoshi", "Satoshi"]
secondary_crypto_terms = [" coin ", " token ", " chain ", " ledger ", "wallet ", " node ", "decentralized", "cold storage", " hodl ", "exchange", " mining "]

coins_with_unique_names = ["Optimism", "Ethereum", "Arbitrum", "Arbitrum Nova", "Moonbeam", "Moonriver", "OKExChain", "Solana", "Wanchain", "OntologyEVM", "Velas", "Kucoin", "Milkomeda", "Milkomeda", "Bitcoin", "IoTex", "Kusama", "Polkadot", "Litecoin", "Klaytn", "Zilliqa", "ThunderCore", "Sifchain", "Elastos", "Algorand", "Thorchain", "Karura", "Tezos", "Ravencoin", "Genshiro", "EthereumClassic", "TomoChain", "Cardano", "zkSync", "VeChain", "Godwoken", "Hedera", "Echelon", "Syscoin", "Kujira"]
coins_with_unique_names = [coin_name.lower() for coin_name in coins_with_unique_names]

db.stackoverflow_question_sums.drop()

for coin in all_coins:

    week = 0
    duplicate_counter = 0

    #if not coin['coin'] == "Polygon":
        #continue

    page = 1
    question_counter = 0
    unique_name_coin = coin["coin"].lower() in coins_with_unique_names

    while True:
        
        time.sleep(1)   

        url = "https://api.stackexchange.com/2.3/search/advanced?page=" + str(page) + "&pagesize=100&order=desc&sort=activity&title=" + coin["coin"] + "&site=stackoverflow"
        
        page += 1

        params = {'key':"Ast9aGRtKRBQK3ibm4Lsvg(("}
   
        response = requests.request("GET", url, params=params)

        json_response = json.loads(response.text)
        print(json_response)
        
        try:
            if json_response["items"] == []:
                break    
        except:
            break

            
        for element in json_response["items"]:
            
            first_term_match = False
            found = False
            
            try:
                
                if element["title"] is not None:
                    element_title = element["title"].lower()
                else: element_title = ""
                
            
                for term in primary_crypto_terms:

                    if term in element_title or unique_name_coin:
                        found = True
                        break
                                 
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
    db.stackoverflow_question_sums.insert_one({'chain': coin["coin"], 'question_counter':int(question_counter)})
    

        







