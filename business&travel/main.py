# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""
from operator import index

import value as value
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://pro.w2m.travel"

browser = webdriver.Firefox(executable_path = "/usr/local/bin/geckodriver")
browser.get(url)


inputElement = browser.find_element_by_id("email")
inputElement.clear()
inputElement.send_keys("business.travel")
inputElement = browser.find_element_by_id("password")
inputElement.clear()
inputElement.send_keys("Busi2016")

inputElement.submit()


element = WebDriverWait(browser,10).until(EC.visibility_of_element_located((
    By.XPATH,'//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]'))).click()


element = browser.find_element_by_xpath('//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]')
element.clear()
element.send_keys("London")

# TODO
# select = Select(browser.find_element_by_name('name'))
# select.select_by_index(index)
# select.select_by_visible_text("London, Greater London, United Kingdom")
# select.select_by_value(value)

element.click()

# element = WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.XPATH,''))).click()

print(browser.current_url) # TRACER

# browser.quit()