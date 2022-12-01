from gnews import GNews
from traceback import print_exc
from pymongo.errors import DuplicateKeyError
from pytickersymbols import PyTickerSymbols
import requests
import json
import re


google_news = GNews(language='en', max_results=10)

stock_data = PyTickerSymbols()
german_stocks = stock_data.get_stocks_by_index('DAX')
uk_stocks = stock_data.get_stocks_by_index('FTSE 100')





word = "hello 69 # ?!,. [{ this is \ta\ttest"
result = re.sub(r'[^A-Za-z0-9.,]+', " ", word) 

print(result)  # prints: hello this is a test



counter = 0
 
with open('articles1215.txt', 'a') as f:

    companies =  ["JP Morgan", "Credit Suisse", "BP", "Braclays", "Google", "Volkswagen", "Bank of America", "HSBC", "Mercedes"]      #"UBS AG", "DHL", "Microsoft",                              #list(german_stocks)

    for company in companies:

        """

        company = company["name"]

        company = company.replace("AG", "")
        company = company.replace("Holding", "")
        company = company.replace("Group", "")
        company = company.replace("SE", "")
        company = company.replace("N.V.", "")
        company = company.replace("PLC", "")
        company = company.replace("KGaA Vz", "")
        company = company.replace("AG & Co. KGaA St", "")


        """

        for chain in ["Polygon", "IOTA", "Solana", "Hyperledger", "Corda", "VeChain", "Ethereum"]:

            news = google_news.get_news('{} AND blockchain AND {}'.format(company, chain))

            for item in news:

                try:

                    if counter == 600:
                        print(counter)
                        f.close()
                        break

                    counter += 1

                    article = google_news.get_full_article(item['url'])
                    print(article.text)

                    pattern = chain
                    match=(re.search(pattern, article.text))

                    lines = article.text.split('\n')
                    cut_articletext = [line for line in lines if line.strip()]

                    for sentence in cut_articletext:

                        if company in sentence and chain in sentence:

                            print(company)
                            print(chain)
                            print(sentence)

                            Collaboration = input('Collaboration?')

                            f.write("{ " + chr(34) + "prompt" + chr(34) + ": " + chr(34) + str(counter) + " / " + str(company) + " / " + str(chain) + " / " + re.sub(r'[^A-Za-z0-9.,]+', " ", sentence)  + " " + " ->END" + chr(34) + ", " + chr(34) + "completion" + chr(34) + ": " + chr(34) + "Collaboration:" + Collaboration + "->END" + chr(34) + " }" + "\n")
                            #f.write("{ " + chr(34) + "prompt" + chr(34) + ": " + chr(34) + str(counter) + " / " + str(company) + " / " + str(chain) + " / " + re.sub(r'[^A-Za-z0-9.,]+', " ", sentence)  + " " + " ->END" + chr(34) + ", " + chr(34) + "completion" + chr(34) + ": " + chr(34) + "Collaboration:" + Collaboration + " /Entity Business:" + input_PB + " /Blockchain:" + input_Chain + "->END" + chr(34) + " }" + "\n")
                        
                            break

                        else:

                            continue


 
                    #cut_articletext = " ".join(cut_articletext)
                    #cut_articletext = re.sub(r'[\W]+', ' ', cut_articletext)

                    #cut_articletitle = article.title
  
                    #f.write("{ " + chr(34) + "prompt" + chr(34) + ": " + chr(34) + str(counter) + " / " + str(company) + " / " + str(chain) + " / " + cut_articletitle + " " + " ->END" + chr(34) + ", " + chr(34) + "completion" + chr(34) + ": " + chr(34) + "BOOL" + " END" + chr(34) + " }" + "\n")
                    #f.write("{ " + chr(34) + "prompt" + chr(34) + ": " + chr(34) + str(counter) + " " + str(company) + " " + str(chain) + " " + cut_articletitle + " " + cut_articletext + " ->END" + chr(34) + ", " + chr(34) + "completion" + chr(34) + ": " + chr(34) + "project: status: company: partners: blockchain:" + " END" + chr(34) + " }" + "\n")
                    #f.write(", " + chr(34) + "completion" + chr(34) + ": " + chr(34) + "project: status: company: partners: blockchain:" + " END" + chr(34) + " }" + "\n")

                    print(counter)

                except Exception as e:
                    print(e)
                    pass
                    





