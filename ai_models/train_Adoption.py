from gnews import GNews
import pymongo
from pymongo.errors import DuplicateKeyError
import re
import os
import openai
import pandas as pd
import datetime
from traceback import print_exc


openai.api_key = os.getenv("OPENAI_API_KEY")

google_news = GNews(language='en', max_results=10)

counter = 0


for company in ["Royal Dutch Shell", "DHL", "JP Morgan"]:

    for industry in ["commodities", "oil", "gas", "distribution", "transportation", "freight", "container", "letters", "banking", "bonds", "shares"]:

                news = google_news.get_news('{} AND blockchain AND {}'.format(company, industry))

                for item in news:

                    with open("./ai_models/prompt_examples_get_Adoption.txt", "a") as f:

                        try:

                            article = google_news.get_full_article(item['url'])
                            article_date = ""

                            article_date = article.publish_date.strftime('%m.%d.%Y')

                            lines = article.text.split('\n')
                            cut_articletext = [line for line in lines if line.strip()]
                                        
                            for sentence in cut_articletext:

                                if "partner" in sentence.lower() or "partner" in sentence.lower() or "collaborating" in sentence.lower() or "working together" in sentence.lower() or "blockchain" in sentence.lower():

                                    if company.lower() in sentence.lower():

                                        print(company)
                                        print(sentence)

                                        Adoption = input("Adoption?")

                                        f.write("input: ### " + company + " ### " + sentence + "#######END#######\n")
                                        f.write("Adoption: " + Adoption + "#######END#######\n")
                                        f.write("====================================\n")        

                        except:
                            pass

                        f.close()

