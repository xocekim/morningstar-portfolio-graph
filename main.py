import re
import sqlite3
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

from mysecrets import USERNAME, PASSWORD

# setup db
con = sqlite3.connect('morningstar.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

# setup selenium
options = webdriver.EdgeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--window-size=1920,1200")
# options.binary_location = """C:\Program Files\Google\Chrome Beta\Application\chrome.exe"""
driver = webdriver.Edge(options=options)
driver.set_window_position(-1000, 0)
driver.maximize_window()
driver.implicitly_wait(5)

driver.get('https://www.morningstar.co.uk/uk/portfoliomanager/start')
time.sleep(1)
try:
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
except NoSuchElementException:
    pass
time.sleep(1)
driver.find_element(By.ID, 'btn_individual').click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, 'div#loginportfolio > a').click()
time.sleep(1)

driver.find_element(By.ID, 'emailInput').send_keys(USERNAME)
driver.find_element(By.ID, 'passwordInput').send_keys(PASSWORD)
driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
time.sleep(1)
table = driver.find_element(By.ID, 'ctl00_ctl00_MainContent_PM_MainContent_gv_Portfolio')
for row in table.find_elements(By.CSS_SELECTOR, 'tr[class$=Item]'):
    share = {}
    tds = row.find_elements(By.CSS_SELECTOR, 'td')
    share_id = tds[0].find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    share['id'] = re.search(r'id=(\w+$)', share_id).group(1)
    share['name'] = tds[0].text
    share['price'] = tds[1].text
    share['quantity'] = tds[4].text
    print(share)
    cur.execute('INSERT INTO history (id, price, quantity) '
                'VALUES (:id, :price, :quantity)', share)
con.commit()


print('done')
