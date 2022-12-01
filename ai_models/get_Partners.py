from gnews import GNews
import pymongo
from pymongo.errors import DuplicateKeyError
import re
import os
import openai
import pandas as pd
import datetime
from traceback import print_exc

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Company:
        pass 


#========================================

def get_Articledate(title):

    for attempt in range(1, 2):

        try:
            driver.get(google_url)
            inputelement = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
            inputelement.send_keys(title)
            inputelement.send_keys(Keys.ENTER)

            article_date = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[11]/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/span[1]/span").text
        except:
            article_date = datetime.datetime.today().strftime('%m.%d.%Y')
            continue

        return article_date  


def get_Companyinfo(raw_partner_name):

    company = Company()

    driver.get(google_url)
    inputelement = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
    inputelement.send_keys(raw_partner_name)
    inputelement.send_keys(Keys.ENTER)

    company_and_additional_info = driver.find_elements(By.CLASS_NAME, "SPZz6b")

    try:
        company.icon = driver.find_element(By.ID, "wp_thbn_52").get_attribute("src")
    except:
        company.icon = "https://opendata.transport.nsw.gov.au/themes/open_data_portal/Previewlogo.png"

    try:
        company.name = company_and_additional_info[0].text.split("\n")[0]
        if "Result" in company.name: raise()
    except:
        company.name = raw_partner_name

    try:
        company.industry = company_and_additional_info[0].text.split("\n")[1]
    except:
        company.industry = industry


    return company



def get_Partners_from_ai(input):
                 
    return openai.Completion.create(
    model="text-curie-001",
    prompt= examples + input,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
 
 #========================================                                       

service_object = Service(binary_path)
options = Options()
options.headless = True

#options=options
driver = webdriver.Chrome(service=service_object)
google_url = "https://www.google.com/"


#connect to db
mongo_client = pymongo.MongoClient({"mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority"})
db = mongo_client["Crypto01"]

db.Blockchain_adoption_chain_partners.drop()
db.Blockchain_adoption_chain_partners.create_index("partner_name") 


openai.api_key = os.getenv("OPENAI_API_KEY")

google_news = GNews(language='en', max_results=10)

counter = 0

with open('./ai_models/prompt_examples_get_Partners.txt', 'r') as f:
    examples = str(f.readlines())
    f.close()


for chain in ["VeChain", "VeChain", "Hyperledger", "Corda", "Polygon", "IOTA", "Ronin", "Immutable X"]:

    for industry in ["mobility", "logistics", "gaming", "mobility", "entertainment", "sports"]:

        for keyword in ["partnering", "collaborating"]:

                news = google_news.get_news('{} AND blockchain AND {} AND {}'.format(chain, industry, keyword))

                for item in news:

                        try:

                            article = google_news.get_full_article(item['url'])
                            article_date = ""

                            print(article.publish_date)

                            print(article.title)

                            article_date = article.publish_date.strftime('%m.%d.%Y')
                                        
                            duplicate_check = db.Blockchain_adoption_chain_partners.find({"$and":[
                                                                                    {"chain":chain},
                                                                                    {"news_url":article.url},
                                                                                    ]})

                            if not len(list(duplicate_check)) == 0: break
                                
                            lines = article.text.split('\n')
                            cut_articletext = [line for line in lines if line.strip()]

                            sentence = str(cut_articletext)

                            #========================================

                            for sentence in cut_articletext:

                                if "partner" in sentence.lower() or "collaborating" in sentence.lower() or "working together" in sentence.lower():

                                    if chain.lower() in sentence.lower():

                                        #========================================
                                        if article_date == "": article_date = get_Articledate(article.title)
                                        #========================================
                       
                                        input_for_ai = "input: ## {} ## ".format(chain) + sentence + "##########END###########\n partnership with:"

                                        get_Partners_from_ai_response = get_Partners_from_ai(input_for_ai)

                                        raw_partner_names = re.sub(r'[^A-Za-z0-9.,&?!èéàüäöç$@]+', " ", get_Partners_from_ai_response["choices"][0]["text"].replace("##########END###########", "")) 

                                        #========================================
                                        
                                        raw_partner_names = raw_partner_names.split(",")

                                        for raw_partner_name in raw_partner_names:

                                            print("first raw partner name: " + raw_partner_name)

                                            if len(raw_partner_name) > 100 or len(raw_partner_name.split(" ")) > 3: break

                                            company = get_Companyinfo(raw_partner_name)

                                            #========================================

                                            print("final company name: " + company.name)
                                            print(company.industry)
                                            print("company icon: " + company.icon)
                                         
                                            db.Blockchain_adoption_chain_partners.insert_one({  "partner_name":company.name,
                                                                                                "partner_industry":company.industry,
                                                                                                "partner_icon":company.icon,
                                                                                                "chain":chain,
                                                                                                "article_url":article.url,
                                                                                                "article_date":article_date                           
                                                                                            })
                                           
                                      

                            print(counter)

                        except Exception as e:
                            print(e)
                            pass

        







