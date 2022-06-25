#Configure logging
import logging,time,json
logging.basicConfig(level=logging.INFO)

import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By #For selecting
from selenium.webdriver.support.ui import WebDriverWait #For waiting for elements to load
from selenium.webdriver.support import expected_conditions as EC #Conditions for waiting

import parser

driver = webdriver.Firefox()
url = "https://www1.nyc.gov/site/ccrb/policy/MOS-records.page"

logging.info(f"Geting main webpage at {url}")
driver.get(url)

#Object I want to parse.
css_selector = ".bodyCells"
time.sleep(2)
#driver.switch_to.default_content() #Default frame
logging.info("Switch to loaded iframe context")
driver.switch_to.frame(1)

logging.info("Wait for object to be on page (This is faster then just waiting arbitrarily)")
try:
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,css_selector)))
except selenium.common.exceptions.TimeoutException:
    pass

logging.info("At this point the data should be loaded")
filename = "content.json"
allContent = []
f = open(filename,'w+') #Overwrite
json.dump(allContent,f) #Write object to file

logging.warning("Press CTRL+C to stop!")
while True:
    try:
        logging.info("Get wrapper")
        element = driver.find_element(By.CSS_SELECTOR,css_selector)

        logging.info("Get table")
        html = element.get_attribute('innerHTML')
        content = parser.parseHtml(html)

        logging.info(f"Writing content to {filename}")
        allContent += content
        json.dump(allContent,f) #Write object to file

        #ScrollDown one window
        driver.execute_script("document.getElementsByClassName('bodyCells')[0].scrollBy(0,document.getElementsByClassName('bodyCells')[0].getBoundingClientRect().height)")
        time.sleep(0.5)
    except KeyboardInterrupt:
        logging.warning("Exiting!")
        json.dump(allContent,f) #Write object to file
        logging.warning("Closing file!")
        f.close()
        logging.warning('Writing dataframe')
        df = parser.getDataFrame(allContent)
        df.to_csv(filename.replace('json','csv'))
        logging.warning("Done!")
        break
