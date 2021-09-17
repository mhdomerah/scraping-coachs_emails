import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriver, ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd

# Open chrome in headless mode and get video count the channel 
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.ncsanj.com/clubTeams.cfm")
page = driver.page_source
soup = BeautifulSoup(page, "html.parser")
values = soup.find_all("option")
coachs = []

for value in values[1:]:
    select = Select(driver.find_element_by_id('clubid'))
    v = str(value).replace('"', ' ').split()[2]
    select.select_by_value(f"{v}")
    driver.find_element_by_css_selector('.gray_btn.select_btn').click()

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table_body = soup.find("tbody")
    try:
        rows = table_body.find_all('tr')
    except:
        pass
    for row in rows:
        coach = {}
        cols=row.find_all('td')
        #cols=[x.text.strip() for x in cols]
        div = cols[2].find("div",{"class":"container"})
        coach["Name"] = div.find("h2").text
        coach["Email"] = div.find("a").text
        coachs.append(coach)

   #driver.quit()    

df = pd.DataFrame(coachs)
df.to_csv("coachs.csv", index = False)
