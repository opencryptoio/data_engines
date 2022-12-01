
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




service_object = Service(binary_path)
options = Options()
options.headless = True

driver = webdriver.Chrome(service=service_object)

#driver.get("https://www.google.ch/")
#inputelement = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
#inputelement.send_keys("Solana unveils Google partnership, smartphones, Web3 store at Breakpoint")
#inputelement.send_keys(Keys.ENTER)


driver.get("https://www.google.ch/search?q=UFC&ei=t0mIY5yhGoCv2roP16iTiAI&ved=0ahUKEwjc2My25df7AhWAl1YBHVfUBCEQ4dUDCBA&uact=5&oq=UFC&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIHCC4Q1AIQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgsILhCABBDHARCvAToLCC4QgAQQxwEQ0QM6CAguEIAEENQCOgUILhCABEoECEEYAEoECEYYAFCgB1inDWC0EGgCcAB4AIAB5gGIAfcEkgEFMC4xLjKYAQCgAQGwAQDAAQE&sclient=gws-wiz-serp")
company = driver.find_element(By.ID, "wp_thbn_52")

print(company.get_attribute("src"))




print(article_date)