#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

url = "https://viajesloreto.com/"

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True


options.add_argument('headless')
pathToFirefoxDriver = "/usr/local/bin/geckodriver"
browser = webdriver.Firefox(executable_path = pathToFirefoxDriver,options=options)
print ("\nHeadless Firefox Initialized\n")

browser.get(url)
counter = 1
# elements = browser.find_elements_by_xpath('//div[1]/div[2]/div[2]/span') # front page prices
elements = browser.find_elements_by_xpath('//div[1]/div[2]/h2/a')
for element in elements:
    if counter < 21:
        print(counter, element.get_attribute("textContent"))
#    print("Names:\n", element.text)

    counter = counter+1

import time

time.sleep(2)
browser.quit()

