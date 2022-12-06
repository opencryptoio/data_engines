from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



service_object = Service(binary_path)
options = Options()
options.headless = True

#options=options

driver = webdriver.Chrome(service=service_object)

google_url = "https://www.google.com/"
driver.get(google_url)
inputelement = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
inputelement.send_keys("JPMorgan")
inputelement.send_keys(Keys.ENTER)

google_url = "https://www.google.com.au/imghp?hl=en&ogbl"
driver.get(google_url)
inputelement = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
inputelement.send_keys("JPMorgan logo")
inputelement.send_keys(Keys.ENTER)


        
print(driver.find_element(By.CLASS_NAME, "bRMDJf.islir").find_element(By.TAG_NAME, "img").get_attribute("src"))
