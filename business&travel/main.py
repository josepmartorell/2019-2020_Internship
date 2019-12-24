# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# url access
url = "https://pro.w2m.travel"
browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
browser.get(url)

# logging
inputElement = browser.find_element_by_id("email")
inputElement.clear()
inputElement.send_keys("business.travel")
inputElement = browser.find_element_by_id("password")
inputElement.clear()
inputElement.send_keys("Busi2016")
inputElement.submit()

# wait to load the search engine
element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((
    By.XPATH,
    '//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]'))).click()
element = browser.find_element_by_xpath(
    '//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]')
element.clear()

# check access
assert "Hotels | W2M" in browser.title
print(browser.current_url)

# enter data in input field
element.send_keys("london")

# TODO:
# drop-down item selection
actions = ActionChains(browser)
for _ in range(3):
    actions.send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(1)

# press button
login_attempt = element.find_element_by_xpath("/html/body/form/div[1]/header/div[2]/div/div/div[2]/div[2]/button")
login_attempt.submit()


# close the browser
time.sleep(6)
browser.quit()

# FIXME:
# when selecting from the drop down before moving three items down
# you have already slowed down two items !!??!?
# or does not select the item or does not press the button, or both...
# tentative solution: build a list with the itmes to then try on it in the for cycle
# you can create a module to do it