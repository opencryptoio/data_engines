from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
import datetime
from datetime import timedelta
import pandas as pd
import pymongo
from traceback import print_exc

mongo_client = pymongo.MongoClient("mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["Crypto01"]

try:
    db.developer.create_index("name", unique=True)  
except Exception as e:
    print(e)
    pass

service_object = Service(binary_path)
driver = webdriver.Chrome(r"C:\ProgramData\Anaconda3\Lib\site-packages\chromedriver_py\chromedriver_win32.exe")

all_commits = pd.DataFrame(db.commits.find())

for dev in set(all_commits['developer']):
    
    try:
    
        dev_commits = all_commits.loc[all_commits['developer'] == dev]
        first_commit = min(dev_commits['commit_date'])
        total_commits = dev_commits['commit_date'].count()
        print(total_commits)

        url = "https://github.com/" + dev.replace(" ", "")

        driver.get(url)

        try:
            followers = driver.find_element(By.XPATH, "//*[@id=" + chr(34) + "js-pjax-container" + chr(34) + "]/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/a[1]/span").text
            
            if "k" in followers or "n" in followers:
                followers = followers.replace("k", "")
                followers = followers.replace("n", "")
                
                if "." in followers:
                    followers = followers.replace(".", "")
                    followers = int(followers) * 100
                else: followers = int(followers) * 1000
                
        except:
            followers = 0
            pass
        
        try:
            location = driver.find_element(By.XPATH, "//*[@id=" + chr(34) + "js-pjax-container" + chr(34) + "/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/ul/li[2]/span").text
        except:
            location = 0
            pass

        db.developer.insert_one({'name': dev, 'first_commit': first_commit, 'total_commits': int(total_commits), 'followers': followers, 'location': location, 'url': url})
        

    except Exception as e:
            print(e)
            print ('type is:', e.__class__.__name__)
            print_exc()
            continue

