# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://pro.w2m.travel"

# options = Options()
# options.add_argument("window-size=1400,600")

# ua = UserAgent()
# user_agent = ua.random

# print(user_agent)

# options.add_argument(f'user-agent={user_agent}')
# browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", options=options)

browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
browser.get(url)

inputElement = browser.find_element_by_id("email")
inputElement.clear()
inputElement.send_keys("business.travel")
inputElement = browser.find_element_by_id("password")
inputElement.clear()
inputElement.send_keys("Busi2016")

inputElement.submit()

element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((
    By.XPATH,
    '//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]'))).click()

element = browser.find_element_by_xpath(
    '//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]')
element.clear()
element.send_keys("London")
# element.click()
# TODO
login_attempt = element.find_element_by_xpath("/html/body/form/div[1]/header/div[2]/div/div/div[2]/div[2]/button")
login_attempt.click()


print(browser.current_url)  # TRACER
import time
time.sleep(20)
browser.quit()
