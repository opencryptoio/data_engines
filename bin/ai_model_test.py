
from gnews import GNews
import pymongo
from pymongo.errors import DuplicateKeyError
import re
import os
import openai
import pandas as pd
from datetime import datetime
from traceback import print_exc

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime

import dateparser
dateparser.parse('12/12/12')


dateparser.parse('2 days ago')








service_object = Service(binary_path)
options = Options()
options.headless = True

driver = webdriver.Chrome(service=service_object)

#driver.get("https://www.google.ch/")
#inputelement = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
#inputelement.send_keys("Solana unveils Google partnership, smartphones, Web3 store at Breakpoint")
#inputelement.send_keys(Keys.ENTER)


driver.get("https://www.google.ch/search?q=Solana+unveils+Google+partnership%2C+smartphones%2C+Web3+store+at+Breakpoint&source=hp&ei=NyqIY-3yIdDc2roPtrOKgAI&iflsig=AJiK0e8AAAAAY4g4RzaLLjAIjBKpvNkAu3TDwxBwaE08&ved=0ahUKEwit6rixx9f7AhVQrlYBHbaZAiAQ4dUDCAk&uact=5&oq=Solana+unveils+Google+partnership%2C+smartphones%2C+Web3+store+at+Breakpoint&gs_lcp=Cgdnd3Mtd2l6EANQAFiCA2DDBGgAcAB4AIABAIgBAJIBAJgBAKABAQ&sclient=gws-wiz")
company = driver.find_elements(By.CLASS_NAME, "Z26q7c UK95Uc")

frame = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[11]/div/div[2]/div[2]/div/div")
date = frame.find_elements(By.CLASS_NAME, "MjjYud")

for element in date:
    print(element.text)

print(company.get_attribute("src"))




print(article_date)