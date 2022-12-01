from gnews import GNews
from traceback import print_exc
from pymongo.errors import DuplicateKeyError
from pytickersymbols import PyTickerSymbols
import requests
import json
import re

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

google_news = GNews(language='en', max_results=100)

counter = 0

for chain in ["Cardano", "VeChain", "Solana", "Hyperledger", "Corda", "Polygon", "IOTA", "Ronin", "Immutable X"]:

    for keyword in ["partnering", "collaborating"]:

            news = google_news.get_news('{} AND blockchain AND government AND {}'.format(chain, keyword))

            for item in news:

                with open('Parters.txt', 'a') as f:

                    try:

                        counter += 1

                        article = google_news.get_full_article(item['url'])

                        pattern = chain
                        match=(re.search(pattern, article.text))

                        lines = article.text.split('\n')
                        cut_articletext = [line for line in lines if line.strip()]

                        sentence = str(cut_articletext)

                        for sentence in cut_articletext:

                        #if "building on" in sentence.lower() or "development company" in sentence.lower() or "foundation behind" in sentence.lower() or "company" in sentence.lower() or "development partner" in sentence.lower():
                        #if "using" in sentence.lower() or "building on" in sentence.lower() or "relying on" in sentence.lower() or "collaborating with" in sentence.lower() or "partnering with" in sentence.lower():
                            if "partner" in sentence.lower() or "collaborating" in sentence.lower() or "working together" in sentence.lower():

                                if chain.lower() in sentence.lower():

                                    f.write(chain + "\n")
                                    f.write(sentence + "\n")

                                    print(chain)
                                    print(sentence)

                                    Partners = input("?")
                                    f.write(Partners + "\n")

                                    f.write("====================================" + "\n")

                                    break

                        print(counter)

                    except Exception as e:
                        print(e)
                        pass

                f.close()
                    





