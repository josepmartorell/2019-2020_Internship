#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# implement headless webdriver
options = Options()
options.headless = True
options.add_argument('headless')
pathToFirefoxDriver = "/usr/local/bin/geckodriver"
browser = webdriver.Firefox(executable_path = pathToFirefoxDriver,options=options)
print ("\nHeadless Firefox Initialized\n")

# access url
url = "https://viajesloreto.com/"
browser.get(url)

# TODO: data extraction
# front page prices
elements = browser.find_elements_by_xpath('//div[1]/div[2]/div[2]/span')
for element in elements:
    price = element.get_attribute("textContent").strip('€')
    if not ',' in price:
        price = price.strip(" ") + ",00"

    print(str(price))

# front page travels
counter = 1
elements = browser.find_elements_by_xpath('//div[1]/div[2]/h2/a')
for element in elements:
    if counter < 21:
        if counter < 10:
            print("", counter, element.get_attribute("textContent"))
        else:
            print(counter, element.get_attribute("textContent"))

    counter = counter+1
#    print("Trip:\n", element.text)


# close navigation session
time.sleep(2)
browser.quit()

# FIXME:
# remove blanks in prices

