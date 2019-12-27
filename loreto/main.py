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
elements = browser.find_elements_by_xpath('//div[1]/div[2]/h2/a')
for element in elements:
    if counter < 21:
        if counter < 10:
            print("", counter, str(display[counter - 1]), element.get_attribute("textContent"))
        else:
            print(counter, str(display[counter - 1]), element.get_attribute("textContent"))
    counter = counter+1

print("\n\nRanking (homepage offers):\n")
# ranking manager
prices = []
elements = browser.find_elements_by_xpath('//div[1]/div[2]/div[2]/span')
# price list
for element in elements:
    element = element.get_attribute("textContent").strip('€')
    if not ',' in element:
        element = element.strip(" ") + ",00"
    element = element.replace(',', '.')
    prices.append(element)
new_prices = []
# convert to float
for element in prices:
    rank = float(element)
    new_prices.append(rank)
counter = 1
places = []
travels = browser.find_elements_by_css_selector('.package-title > a:nth-child(1)')
counter = 1
# travel list
for travel in travels:
    if counter < 21:
        places.append(travel.get_attribute("textContent"))
#        print(element.get_attribute("textContent"))
    counter = counter + 1
# final list
list = dict(zip(prices, places))
# todo: sorting list
ranking = sorted(list.items())
for k, v in ranking:
#    print("{0:.2f}".format(element))
    print(k, v)



#ranking = dict(zip(list, list2))
#print(ranking)

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
