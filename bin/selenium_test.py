from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

service_object = Service(binary_path)
# instance of Options class allows
# us to configure Headless Chrome
options = Options()

# this parameter tells Chrome that
# it should be run without UI (Headless)
options.headless = True

list = [1,2,3]

arrstring = "ABCD".split(",")

print(len(arrstring))

if list:
    print("not empty")
else:
    print("empty")

# initializing webdriver for Chrome with our options options=options
driver = webdriver.Chrome(service=service_object, options=options)
driver.get("https://www.google.ch/")

# getting GeekForGeeks webpage
inputelement = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
inputelement.send_keys("Gamestop")
inputelement.send_keys(Keys.ENTER)

companies = driver.find_elements(By.CLASS_NAME, "SPZz6b")

try:
    print(companies[0].text)
except IndexError as e:
    print("Company not found")







# close browser after our manipulations
driver.close()
