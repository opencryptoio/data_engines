
import os
import openai
import re
from gnews import GNews
from traceback import print_exc
import requests
import re
import json


counter = 0

google_news = GNews(language='en', max_results=100)

openai.api_key = os.getenv("OPENAI_API_KEY")


for company in ["Amazon", "BMW", "Meta", "Maersk", "Commonwealth Bank"]:
    
    
    for chain in ["Solana", "Corda", "Hyperledger", "Ethereum", "Moonriver", "Ripple", "Cardano", "Polkadot"]:


          with open('articles2332.txt', 'a') as f:

            news = google_news.get_news('{} AND blockchain AND {}'.format(company, chain))

            for item in news:

                try:

                    if counter == 20:
                      f.close()
                      break
                      

                    counter += 1

                    article = google_news.get_full_article(item['url'])
                    pattern = chain
                    match=(re.search(pattern, article.text))
                    
                    cut_articletext = article.text[match.span()[0]-5000:match.span()[1]+5000]
                    lines = cut_articletext.split('\n')

                    cut_articletext = [line for line in lines if line.strip()]

                    for sentence in cut_articletext:

                        if company in sentence and chain in sentence:

                    cut_articletitle = article.title

                    #f.write("{ " + chr(34) + "prompt" + chr(34) + ": " + chr(34) + str(counter) + " " + cut_articletitle + " " + cut_articletext + " ->END" + chr(34) + ", " + chr(34) + "completion" + chr(34) + ": " + chr(34) + "project: status: company: partners: blockchain:" + " END" + chr(34) + " }" + "\n")
                    #f.write(", " + chr(34) + "completion" + chr(34) + ": " + chr(34) + "project: status: company: partners: blockchain:" + " END" + chr(34) + " }" + "\n")

                    
                    ai_response = openai.Completion.create(
                    model="curie:ft-personal-2022-11-29-01-52-01 ",
                    prompt= cut_articletitle + cut_articletext + "#####END#####",
                    temperature=0,
                    max_tokens=64,
                    top_p=0.4,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                    )

                    ai_response = json.dumps(ai_response)
                    ai_response = json.loads(ai_response)

                    print(ai_response["choices"][0]["text"])

                    f.write("========================" + "\n")

                    f.write(cut_articletitle + "\n")
                    writetext = str(ai_response["choices"][0]["text"])
                    f.write(writetext + "\n")

                    print(writetext)

                except Exception as e:
                    print(e)
                    pass
                    
            f.close()






