import requests
import json
import pymongo
import time
from bson.objectid import ObjectId
from datetime import datetime
from datetime import timedelta
from pymongo.errors import DuplicateKeyError
import pandas as pd


mongo_client = pymongo.MongoClient("mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["Crypto01"]

all_repositories = db.repositories.find({})

query_date = datetime.today() - timedelta(days=0)
coin_query = {'commit_scrape_date': {'$lt': str(query_date.isoformat())}}
all_repositories = db.repositories.find(coin_query)

try:
    db.commits.create_index("sha", unique=True)  
except Exception as e:
    print(e)
    pass

for repository in all_repositories:
    
    week = 0
    empty_counter = 0
    lastpage = False
    branches = []
    page = 1

    db.repositories.update_one({'_id': ObjectId(repository["_id"])}, {'$set': {'commit_scrape_date': datetime.today().isoformat()}})
    
    #get all branches
    
    while lastpage == False:
            
           try:
           
                time.sleep(1)
                url = repository["url"] + "/branches?per_page=100&page=" + str(page)
                page = page + 1
                
                payload={}
                headers = {
                    'Authorization': 'token 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'
                }
                
                response = requests.request("GET", url, headers=headers, data=payload)
        
                json_response = json.loads(response.text)
                
                if json_response == [] or "message" in json_response or page > 100:
                    break
                else: 
                    pass
                
                for element in json_response:
            
                    branches.append(str(element['commit']['sha']))
            
           except:
               continue      
    
    duplicate_counter = 0
        
    for branch in branches:
        
            lastpage = False
            page = 1
        
            while lastpage == False and duplicate_counter < 10:
        
                url = repository["url"] + "/commits?per_page=100&page=" + str(page) + "&sha=" + branch
                print(url)
                page = page + 1
                
                payload={}
                headers = {
                    'Authorization': 'token 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'
                }
                
                response = requests.request("GET", url, headers=headers, data=payload)

                json_response = json.loads(response.text)
                
                if json_response == [] or "message" in json_response:
                    break
                else: 
                    pass
                
                try:

                    for element in json_response:
                        
                        try:
                            db.commits.insert_one({'sha': element["sha"], 'developer': element["commit"]["author"]["name"], 'repository': repository["url"], 'commit_date': element["commit"]["author"]["date"], 'commit_scrape_date': datetime.today().isoformat()})
                            empty_counter += 1
                            print("added: " + element["sha"] + " / " + element["commit"]["author"]["email"] + "/repository: " + repository["url"])
                            duplicate_counter = 0
                            
                        except DuplicateKeyError as de:
                        
                            print("dublicate: " + repository["url"] + " / " + element["commit"]["author"]["email"] + " / " + element["commit"]["author"]["date"])
                            
                            duplicate_counter += 1
                            
                            if duplicate_counter == 10:
                                break
                            
                            continue

                    
                except:
                    continue
                        

            
            
