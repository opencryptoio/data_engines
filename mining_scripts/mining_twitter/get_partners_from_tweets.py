
from gnews import GNews
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
import time
import openai
import json
import dateparser
import pandas as pd
import random
from snscrape.modules import twitter
import re
from datetime import timedelta
from datetime import datetime



service_object = Service(binary_path)
options = Options()
options.headless = False

driver = webdriver.Chrome(service=service_object, options=options)

google_url = "https://www.google.ch/search?q="
twitter_url = "https://twitter.com/"


def get_company(twitterusername):

    completed = False

    for attempt in range(1, 2):

        company = Company()



        if completed == True:
            break

        try:

            twitterusername = twitterusername.replace("#", "").replace(" ", "_")
            checked_twittername = ""

            if not "@" in twitterusername:
                
                driver.get(google_url + twitterusername.replace(" ", "+") + "+twitter")
                time.sleep(2)

                for attempt_get_link in range(0, 4):

                    try:
                        linktitle = driver.find_elements(By.CLASS_NAME, "LC20lb.MBeuO.DKV0Md")[attempt_get_link].text
                        print("getting linktitle: " + linktitle)
                        res = re.search(r'\(.*?\)', linktitle)
                        checked_twittername = linktitle[res.regs[0][0]+1:res.regs[0][1]-1]
                    except: pass
                    if not checked_twittername == "":
                        break

                attempt_get_link = 0

                if checked_twittername == "":

                    for attempt_get_link in range(0, 4):
                        
                        try:
                            linktitle = driver.find_elements(By.CLASS_NAME, "LC20lb.MBeuO.xvfwl")[attempt_get_link].text
                            print("getting linktitle: " + linktitle)
                            res = re.search(r'\(.*?\)', linktitle)
                            checked_twittername = linktitle[res.regs[0][0]+1:res.regs[0][1]-1]
                        except: pass
                        if not checked_twittername == "":
                            break
                
                attempt_get_link = 0

                if checked_twittername == "":

                    for attempt_get_link in range(0, 4):
                        
                        try:
                            linktitle = driver.find_elements(By.CLASS_NAME, "haz7je")[attempt_get_link].text
                            print("getting linktitle: " + linktitle)
                            res = re.search(r'\(.*?\)', linktitle)
                            checked_twittername = linktitle[res.regs[0][0]+1:res.regs[0][1]-1]
                        except: pass
                        if not checked_twittername == "":
                            break
            
                twitterusername = checked_twittername

            element = twitter.TwitterUserScraper(twitterusername.replace("@", "").strip(), False)
            time.sleep(2)
            print(element.entity.followersCount)
            company.followers = element.entity.followersCount
            company.friends = element.entity.friendsCount
            company.favourites = element.entity.favouritesCount
            company.mediacount = element.entity.mediaCount
            company.location = element.entity.location
            company.name = element.entity.displayname
            company.icon = element.entity.profileImageUrl

            completed = True

        except Exception as e:
            print(e)
            time.sleep(random.randint(3, 5))
            continue

        return company



class Company:
    pass 


df = pd.DataFrame([], columns=['raw name', 'name', 'followers', 'icon', 'industry', 'friends', 'favourites', 'mediacount', 'location'])

driver = webdriver.Chrome(service=service_object, options=options)

mongo_client = pymongo.MongoClient({"mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority"})
db = mongo_client["Crypto01"]

db.BA_partners.drop()
db.BA_partners.create_index("partner_name") 

previouscompanies = {}
counter = 0

openai.api_key = "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"

with open("get_tweets2.txt", "r") as f:

    alltext = "\n".join(f.readlines())

    rawtweets = alltext.split("========================================")

    counter = 0

    for rawtweet in rawtweets:

        if counter <= 1: 
            counter += 1
            continue

        
        try:

            chain = rawtweet.split("//")[1]

            #if not chain == "polygon": continue

            tweetdate = rawtweet.split("//")[2]
            tweetcontent = rawtweet.split("//")[3].replace("#", "")

            #if not "oasis".lower() in tweetcontent: continue

            input_for_ai = "Tweet to analyze:\n\n" + rawtweet + "\n========================================\n\nindustries: Telecommunications, Logistics, Sports, Entertainment, Fashion, Sustainability, NGO, Government, Technology, Banking, Insurance, unknown\n\nWhich companies are explicitly partnering or collaborating with Coardano according to the \"Tweet to analyze\"? The name of the company has to be in the \"Tweet to analyze\". Rumors do not qualify as explicit partnerships or collaborations. Also exclude the large Social Media companies if there is not an explicit partnership or collaboration.\n\nThe industry of the company has to be in the list \"industries\".\n\nFormat of response: [{\\\"company\\\":Company1,\\\"industry\\\":\\\"Industry1\\\",\\\"blockchaincompany\\\":\\\"Yes1\\\"},{\\\"company\\\":Company2,\\\"industry\\\":\\\"Industry2\\\",\\\"blockchaincompany\\\":\\\"Yes2\\\"},{\\\"company\\\":Company3,\\\"industry\\\":\\\"Industry3\\\",\\\"blockchaincompany\\\":\\\"No3\\\"},etc.....]"
    
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt= input_for_ai,
                temperature=0.0,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["###END###"]
            )

            partners = response["choices"][0]["text"].replace("Answer:", "").replace("Response:", "").strip()

            partners = json.loads(partners)
        except Exception as e:
           continue

        for partner in partners:

            try:
                driver.quit()
            except: pass
            driver = webdriver.Chrome(service=service_object, options=options)

            try:

                with open("found_partners.txt", "a") as f_found_partners:

                    raw_partner_name = partner["company"]
                    raw_partner_industry = partner["industry"]
                    raw_partner_blockchaincompany = partner["blockchaincompany"]

                    #========================================

                    if len(raw_partner_name) > 100 or len(raw_partner_name.split(" ")) > 10: continue
                    if "No partnership or collaboration found" in raw_partner_name: break
                    if "Ergebnisse" in raw_partner_name: continue
                    if chain.lower() in raw_partner_name.lower(): continue

                    #========================================

                    if raw_partner_name in df['raw name'].values:
                        company.name = df.loc[df['raw name'] == raw_partner_name]['name'][0]
                        company.followers = df.loc[df['raw name'] == raw_partner_name]['followers'][0]
                        company.icon = df.loc[df['raw name'] == raw_partner_name]['icon'][0]
                        company.friends = df.loc[df['raw name'] == raw_partner_name]['friends'][0]
                        company.favourites = df.loc[df['raw name'] == raw_partner_name]['favourites'][0]
                        company.mediacount = df.loc[df['raw name'] == raw_partner_name]['mediacount'][0]
                        company.location = df.loc[df['raw name'] == raw_partner_name]['location'][0]
   

                    else: 
                        company = get_company(raw_partner_name)
                        df.loc[len(df.index)] = [raw_partner_name, company.name, company.followers, company.icon, raw_partner_industry, company.friends, company.favourites, company.mediacount, company.location]
                        

                    tweetdate = dateparser.parse(tweetdate).strftime('%d.%m.%Y')

                    if ".2023" in tweetdate:
                        tweetdate = (datetime.strptime(tweetdate, '%d.%m.%Y') - timedelta(days = 365)).strftime('%d.%m.%Y')

                    print(chain)
                    print(company.name)
                    print(company.followers)
                    print(company.icon)
                    print(company.friends)
                    print(company.favourites)
                    print(company.mediacount)
                    print(company.location)
                    print(raw_partner_name)
                    print(raw_partner_industry)

                    if company.location == None: company.loation = "-"

                    db.BA_partners.insert_one({ "partner_name":company.name,
                                                "partner_industry":raw_partner_industry,
                                                "partner_blockchaincompany":raw_partner_blockchaincompany,
                                                "partner_followers":int(company.followers),
                                                "partner_friends": int(company.friends),
                                                "partner_favourites": int(company.favourites),
                                                "partner_mediacount": int(company.mediacount),
                                                "partner_location": company.location,
                                                "partner_icon":company.icon,
                                                "chain_entity":chain,
                                                "tweet_date":tweetdate,
                                                "tweet_content":tweetcontent,                         
                                            })
                                            
                    print("____________")
                    print(counter)
                    print(tweetcontent)
                    print(raw_partner_name)
                    print(company.name)
                    print(raw_partner_industry) 

                                            
                    f_found_partners.write(chain + " / " + str(tweetdate) + " / "  + str(tweetcontent) + " / " + raw_partner_name + "\n")
                
                    f_found_partners.close()

            except Exception as e:
                print(e)
                continue

            


