#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""


import time
import operator
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
# front page prices scraper
display = []
prices = []
elements = browser.find_elements_by_xpath('//div[1]/div[2]/div[2]/span')
for element in elements:
    price = element.get_attribute("textContent").strip('€')
    if len(price) == 6:
        price = " " + price
    if not ',' in price:
        price = price.strip(" ") + ",00 "
    display.append(price)
    price = price.replace(',', '.')
    prices.append(price)

print("\nDisplay (homepage offers):\n")

# display (homepage offers)
counter = 1
places = []
elements = browser.find_elements_by_xpath('//div[1]/div[2]/h2/a')
for element in elements:
    if counter < 21:
        if counter < 10:
            print("", counter, str(display[counter - 1]), element.get_attribute("textContent"))
        else:
            print(counter, str(display[counter - 1]), element.get_attribute("textContent"))
        places.append(element.get_attribute("textContent"))
    counter = counter+1

print("\n\nRanking (homepage offers):\n")

# float cast
new_prices = []
for element in prices:
    rank = float(element)
    new_prices.append(rank)

# final list
list = dict(zip(places, new_prices))
ranking = sorted(list.items(), key=operator.itemgetter(1))
for k, v in ranking:
    if v < 100.00:
        print("", "{0:.2f}".format(v), k)
    else:
        print("{0:.2f}".format(v), k)

# close navigation session
time.sleep(2)
browser.quit()

# FIXME:
# remove blanks in prices
# clear and order the prices list
# format prices adding whitespaces
# create float price list
# create trip list
# ranking outputs 14 items instead of 20
# sort final list by keys
