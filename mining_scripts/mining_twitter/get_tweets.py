import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
import time
import openai


service_object = Service(binary_path)
options = Options()
options.headless = False

driver = webdriver.Chrome(service=service_object)


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

parameters = {
    'sort': 'cmc_rank',
    'limit': '200',
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '7ee264b7-2b6f-4ffd-8e11-5d8f72733981',
}

session = Session()
session.headers.update(headers)

try:

  response = session.get(url, params=parameters)
  data = json.loads(response.text)

  for element in data["data"]:

    url_info = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'

    parameters_info = {
        'slug': element["slug"],
    }

    print(element)

    session = Session()
    session.headers.update(headers)

    try:

        if "bitcoin" == element["slug"].lower(): continue
        if "ethereum" == element["slug"].lower(): continue
        if "tether" == element["slug"].lower(): continue

        response_info = session.get(url_info, params=parameters_info)
        data_info = json.loads(response_info.text)

        twitterusername = data_info["data"][str(element["id"])]["urls"]["twitter"][0]
        twitterusername = twitterusername.replace("https://twitter.com/", "")

        #if "tron" in element["slug"].lower(): twitterusername = "tron"
        #if "polygon" in element["slug"].lower(): twitterusername = "polygon"
        #if "vechain" in element["slug"].lower(): twitterusername = "vechain"
        #if "polkadot" in element["slug"].lower(): twitterusername = "polkadot"


        service_object = Service(binary_path)
        options = Options()
        options.headless = True

        driver = webdriver.Chrome(service=service_object)

        id = int(element["id"])

        if id <= 10: retweet_amount = "10"
        if id > 10: retweet_amount = "5"

        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        counter = 0

        for dateiteration in range (0, 18):

            counter = 0

            until = datetime.today() + relativedelta(months=-dateiteration * 3)
            until = until.strftime('%Y-%m-%d')
            start = datetime.today() + relativedelta(months=-(dateiteration * 3 + 3))
            start = start.strftime('%Y-%m-%d')

            dateiteration += 3

            geturl = "https://twitter.com/search?q=(partnership%20OR%20partnering%20OR%20collaborating%20OR%20joint%20OR%20venture%20OR%20ecosystem)%20(from%3A{})%20until%3A{}%20since%3A{}&src=typed_query&f=top".format(twitterusername, until, start)

            driver.get(geturl)

            time.sleep(2)

            try:
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]").click()
            except Exception as e:
                pass 

            time.sleep(1)
        
            writecounter = 0
            previoustweets = []

            end = False
            
            while end == False:

                for x in range (0, 6):

                    with open(r"get_tweets2.txt", "a") as f:

                        try:

                            counter += 1

                            if counter >= 20: 
                                end = True
                                break

                            time.sleep(0.25)

                            tweet_date = driver.find_elements(By.CLASS_NAME, "css-1dbjc4n.r-18u37iz.r-1q142lx")[x]
                            tweet = driver.find_elements(By.CLASS_NAME, "css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0")[x]

                            if tweet.text[:20] in previoustweets: continue

                            print(tweet_date.text)
                            print(tweet.text)
                            print(until)

                            previoustweets.append(tweet.text[:20])

                            f.write("//" + element["slug"] + "//" +  tweet_date.text + "//" + tweet.text.replace("\n", "") + "\n========================================\n")
                            counter = 0

                        except Exception as e:
                            print(e)
                            continue

                    f.close() 

                driver.execute_script("window.scrollBy(0,1600)","")   

    except Exception as e:
        print(e)
        pass

except Exception as e:
        print(e)
        pass
            

