
from gnews import GNews
import pymongo

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime


list1 = ["1","2","3","4","5"]

list1string = ", ".join(list1)
print(list1string)



service_object = Service(binary_path)
options = Options()
options.headless = True

driver = webdriver.Chrome(service=service_object)

driver.get("https://www.google.ch/search?q=Cryptocurrencies+have+had+a+tough+year%2C+with+STEPN+%28GMT%29+being+one+of+those+taking+the+brunt+of+the+decline.+However%2C+there+is+still+hope+for+crypto+investors+as+BudBlockz+%28BLUNT%29+offers+a+new+way+to+benefit+from+the+digital+asset+mov&sxsrf=ALiCzsaZYAcTAXUX9b1L55UeGf-7KJdMJw%3A1670133130657&ei=ijWMY8TcJ9iG2roP1va-CA&oq=Cryptocurrencies+have+had+a+tough+year%2C+with+STEPN+%28GMT%29+being+one+of+those+taking+the+brunt+of+the+decline.+However%2C+there+is+still+hope+for+crypto+investors+as+BudBlockz+%28BLUNT%29+offers+a+new+way+to+benefit+from+the+digital+asset+mov&gs_lcp=ChNtb2JpbGUtZ3dzLXdpei1zZXJwEANKBAhBGABQAFgAYLZsaABwAHgAgAEAiAEAkgEAmAEAwAEB&sclient=mobile-gws-wiz-serp")
dates = driver.find_element(By.CLASS_NAME, "MUxGbd.wuQ4Ob.WZ8Tjf")

for date in dates:
    print(date.text)


driver.get("https://www.google.ch/search?q=coca+cola&ei=EzeMY9zXOvnc2roP6ceUoAM&ved=0ahUKEwicrbGbpN_7AhV5rlYBHekjBTQQ4dUDCA8&uact=5&oq=coca+cola&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIHCC4Q1AIQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBAgAEEMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgoIABBHENYEELADOgoILhDHARDRAxBDOg4ILhCABBDHARDRAxDUAjoLCC4QgAQQxwEQ0QM6CAguEIAEENQCOgUILhCABDoECC4QQzoLCC4QgAQQxwEQrwE6CgguEIAEENQCEAo6BwguEIAEEApKBAhBGABKBAhGGABQrRFY6CRg5yloBHABeACAAdcCiAG4FZIBBTItNi40mAEAoAEBsAEAyAECwAEB&sclient=gws-wiz-serp")



dates = driver.find_element(By.CLASS_NAME, "MUxGbd.wuQ4Ob.WZ8Tjf")

for date in dates:
    print(date.text)