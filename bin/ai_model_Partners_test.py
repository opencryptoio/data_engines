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

with open('./ai_models/input.txt', 'r') as f:
    examples = str(f.readlines())
    
    f.close()

for chain in ["Polygon", "VeChain", "Solana", "Hyperledger", "Corda", "Polygon", "IOTA", "Ronin", "Immutable X"]:

    for keyword in ["partnering", "collaborating"]:

            news = google_news.get_news('{} AND blockchain AND banking AND {}'.format(chain, keyword))

            for item in news:

                    try:

                        counter += 1

                        article = google_news.get_full_article(item['url'])

                        lines = article.text.split('\n')
                        cut_articletext = [line for line in lines if line.strip()]

                        sentence = str(cut_articletext)

                        for sentence in cut_articletext:

                          with(r"./ai_models/get_Partners_responses.txt", "a") as f:

                            if "partner" in sentence.lower() or "collaborating" in sentence.lower() or "working together" in sentence.lower():

                                if chain.lower() in sentence.lower():

                                    input = "input: ## {} ## ".format(chain) + sentence + "##########END###########\n partnership with:"

                                    response = openai.Completion.create(
                                      model="text-curie-001",
                                      prompt= examples + input,
                                      temperature=0.7,
                                      max_tokens=256,
                                      top_p=1,
                                      frequency_penalty=0,
                                      presence_penalty=0
                                    )

                                    print(chain)
                                    print(sentence)
                                    print(response)

                                    f.write(response["choices"][0]["text"] + "\n")

                                    f.write("========================" + "\n")


                        print(counter)

                    except Exception as e:
                        print(e)
                        pass

    







