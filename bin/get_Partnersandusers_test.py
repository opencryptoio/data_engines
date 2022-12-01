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

with open('./ai_models/input.txt') as f:
    examples = str(f.readlines())
    
    f.close()

print(examples)


 
industries = ["gaming", "entertainment", "nft", "logistics", "mining", "banking", "finance", "mobility"]

for industry in industries:

    keywords =  ["collaboration", "partner", "using", "building", "relying"]      #"UBS AG", "DHL", "Microsoft",                              #list(german_stocks)

    for keyword in keywords:

        for chain in ["Ronin", "Immutable X", "Solana", "Flow", "Ethereum", "Hyperledger", "Corda", "VeChain", "Polygon", "IOTA"]:

                news = google_news.get_news('{} AND {} AND {} AND blockchain'.format(industry, chain, keyword))

                for item in news:

                    with open('partersanusers.txt', 'a') as f:

                        try:

                            counter += 1

                            article = google_news.get_full_article(item['url'])
                            print(article.text)

                            pattern = chain
                            match=(re.search(pattern, article.text))

                            lines = article.text.split('\n')
                            cut_articletext = [line for line in lines if line.strip()]

                            for sentence in cut_articletext:

                                if "partnering" in sentence or "partnership" in sentence or "collaborating" in sentence or "collaboration" in sentence:

                                    if chain in sentence:

                                        input = "input: \\/ {} \\/".format(chain) + sentence + "->END\n\nCollaboration with:"

                                        response = openai.Completion.create(
                                        model="text-curie-001",
                                        prompt= examples + input,
                                        temperature=0.7,
                                        max_tokens=256,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0
                                        )

                                        f.write(chain + "\n")
                                        f.write(sentence + "\n")
                                        f.write(response["choices"][0]["text"] + "\n")
                                        f.write("====================================" + "\n")
    
                                        break

                            print(counter)

                        except Exception as e:
                            print(e)
                            pass

                    f.close()
                        





