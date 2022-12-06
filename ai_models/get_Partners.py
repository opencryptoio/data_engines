from gnews import GNews
import pymongo
from pymongo.errors import DuplicateKeyError
import re
import os
import openai
import pandas as pd
import datetime
from traceback import print_exc
import dateparser
import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path
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

            #/html/body/div[3]/div[2]/div/div[6]/div[3]/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/span/span

            article_date = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[11]/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/span[1]/span").text
    
        except Exception as e:
            print(e)
            article_date = "Today"
            pass

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
    model="text-davinci-003",
    prompt= examples_get_partners_ai + input,
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    )

def get_Partner_result_check(input):
                 
    return openai.Completion.create(
    model="text-davinci-003",
    prompt= "list of companies:  Mercedes Benz, EY, Coinbase, Puma\nnew company: Mercedes ###END###\nclosest match in list of companies: Mercedes Benz ###END###\n\nlist of companies: BMW Group, JPMorgan, DHL, BP\nnew company: DHL ###END###\nclosest match in list of companies: DHL ###END###\n\nlist of companies: Adidas, UBS, Shell, Nike\nnew company: According to the latest report on th 13.03 ###END###\nclosest match in list of companies: This doesnt appear to be a company name ###END###\n\nlist of companies: Adidas, UBS, Shell, Nike\nnew company: Erfolgreich abgeschlossen: ###END###\nclosest match in list of companies: This doesnt appear to be a company name ###END###\n\nlist of companies: BMW Group, PriceWaterhouseCoopers (PWC), Apple, Amazon\nnew company: Nokia ###END###\nclosest match in list of companies: Nokia ###END###\n\nlist of companies:\nnew company: Nokia ###END###\nclosest match in list of companies: Nokia ###END###\n\nlist of companies: Meta\nnew company: Twitter ###END###\nclosest match in list of companies: Twitter ###END###\n\nlist of companies: Twitter, Meta\nnew company: Golden Guild ###END###\nclosest match in list of companies: Golde Guild ###END###\n\nlist of companies: Saudi Aramco, Exxon Mobile\nnew company: BP ###END###\nclosest match in list of companies: BP ###END###\n\n==========================\n" + input,
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
driver.get(google_url)


#connect to db
mongo_client = pymongo.MongoClient({"mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority"})
db = mongo_client["Crypto01"]


#db.BA_partners.drop()
#db.BA_partners.create_index("partner_name") 


openai.api_key = "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"

google_news = GNews(language='en', max_results=100)

counter = 0

with open('./ai_models/prompt_examples_get_partners2.txt', 'r') as f:
    examples_get_partners_ai = str(f.readlines())
    f.close()

with open('./ai_models/prompt_examples_check_partners_result.txt', 'r') as f:
    examples_check_partners_ai = str(f.readlines())
    f.close()


for chain in ["IOTA", "Polkadot", "Web 3 Foundation", "Hyperledger", "Corda", "IOTA", "Ronin", "Immutable X"]:

    partners = []

    for industry in ["mobility", "auto", "electro", "sustainable", "logistics"]:

        for keyword in ["partner"]:

                news = google_news.get_news('{} AND blockchain AND {} AND {}'.format(chain, industry, keyword))

                for item in news:

                    with open("train_get_partners.jsonl", "a") as f_get_partners:
                        with open("train_check_parners.jsonl", "a") as f_check_partners:

                            try:

                                threadcomplete = False
                                threaditerationcounter = 0

                                article = google_news.get_full_article(item['url'])
                                article_date = ""

                                """

                                def thread_function():
                                    article = google_news.get_full_article(item['url'])
                                    
                                    return article

                                thread = threading.Thread(target=thread_function)
                                thread.start()

                                while article is None:
                                    time.sleep(3)
                                    threaditerationcounter += 1

                                    if threaditerationcounter > 20:
                                        break

                                """
                             
                                    
                                print(chain)
                                print(article.url)

                                try:   
                                    duplicate_check = db.BA_partners.find({"$and":[
                                                                                {"chain":chain},
                                                                                {"article_url":article.url},
                                                                                ]})
                                except: pass

                                if not len(list(duplicate_check)) == 0: 
                                    break
                                    
                                lines = article.text.split('\n')
                                cut_articletext = [line for line in lines if line.strip()]

                                sentence = str(cut_articletext)

                                #========================================

                                merged_sentence = ""
                                sentence_counter = 0

                                for sentence in cut_articletext:

                                    if sentence_counter < 3:
                                        merged_sentence = merged_sentence + '.' + sentence
                                        sentence_counter += 1
                                        continue

                                    sentence = merged_sentence
                                    merged_sentence = ""
                                    sentence_counter = 0

                                    if "partner" in sentence.lower() or "collaborating" in sentence.lower() or "working together" in sentence.lower():

                                        if chain.lower() in sentence.lower():

                                            #========================================
                                            if article_date == "": article_date = get_Articledate(article.title)
                                            article_date = dateparser.parse(article_date).strftime('%d.%m.%Y')
                                            #========================================
                        
                                            input_for_ai = "text to analyze: ## {} ## ".format(chain) + sentence + "####END####\n Which companies are partnering or collaborating with {}?:".format(chain)

                                            get_Partners_from_ai_response = get_Partners_from_ai(input_for_ai)

                                            raw_partner_names = re.sub(r'[^A-Za-z0-9.,&?!èéàüäöç$@]+', " ", get_Partners_from_ai_response["choices"][0]["text"].replace("##########END###########", "")) 

                                            #========================================
                                            
                                            raw_partner_names = raw_partner_names.split(",")

                                            for raw_partner_name in raw_partner_names:

                                                raw_partner_name = raw_partner_name.strip().replace(" END", "")

                                                #========================================

                                                if len(raw_partner_name) > 100 or len(raw_partner_name.split(" ")) > 10: break
                                                if "No partnership or collaboration found" in raw_partner_name: break
                                                if "Ergebnisse" in raw_partner_name: break
                                                if chain in raw_partner_name: break

                                                #========================================

                                                company = get_Companyinfo(raw_partner_name)

                                                input_for_ai = "\n\nlist of companies: " + ", ".join(partners) + "\n" + "new company: " + company.name + "###END###" + "\n" + "closest match in list of companies: " 

                                                print(input_for_ai)

                                                if len(company.name) > 5:
                                                    if not company.name.strip() in partners:
                                                        checked_name = get_Partner_result_check(input_for_ai)
                                                        checked_name = checked_name["choices"][0]["text"].replace("###END###", "")
                                                        f_check_partners.write("{list of companies: " + ", ".join(partners) + "new company: " + company.name + "###END###" + "closest match in list of companies: " + checked_name.strip() + "###END###}" + "\n")
                                                    else: checked_name = company.name
                                                else: checked_name = company.name

                                                if "This doesnt appear to be a company name" in checked_name: break

                                                print("checked name by AI: " + checked_name)


                                                #========================================

                                                print("Raw company name: " + raw_partner_name)
                                                print("Compnay Name from Google: " + company.name)
                                                print("checked name by AI: " + checked_name)
                                                
                                                print(company.industry)
                                                print("company icon: " + company.icon)
                                                print(chain)
                                                print(industry)

                                                if not checked_name.strip() in partners: partners.append(checked_name.strip())
                                            
                                                db.BA_partners.insert_one({ "partner_name":company.name,
                                                                            "partner_industry":company.industry,
                                                                            "partner_icon":company.icon,
                                                                            "chain":chain,
                                                                            "article_url":article.url,
                                                                            "article_date":article_date                           
                                                                        })
                                            
                                            f_get_partners.write("{" + "Text to analyze: ## {} ## ".format(chain) + sentence + "###END###" + "Which companies are partnering or collaborating with {}?: ".format(chain) + ",".join(raw_partner_names) + "###END###}" + "\n")

                                print(counter)

                            except Exception as e:
                                print(e)
                                pass

                            f_check_partners.close()
                        f_get_partners.close()

        







