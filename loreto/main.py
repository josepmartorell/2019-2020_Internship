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

# TODO: data extraction (home-page tracking) 1
# access url
url = "https://viajesloreto.com/"
browser.get(url)

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

print("\nRanking (homepage offers):\n")

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

# todo: sub-domain tracking 2
# access url
url_2 = "https://viajesloreto.com/salidas-especiales-puentes/"
browser.get(url_2)

# special-departures-bridges prices scraper
display_2 = []
prices_2 = []
elements = browser.find_elements_by_css_selector('.package-info span.package-price')
for element in elements:
    price = element.get_attribute("textContent").strip('€')
    if len(price) == 6:
        price = " " + price
    if not ',' in price:
        price = price.strip(" ") + ",00 "
    display_2.append(price)
    price = price.replace(',', '.')
    prices_2.append(price)

print("\nDisplay (special-departures-bridges):\n")

# display (special-departures-bridges)
counter = 1
places_2 = []
elements = browser.find_elements_by_css_selector('.package-title-wrapper h2.package-title a')
for element in elements:
    if counter < 14:
        if counter < 10:
            print("", counter, str(display_2[counter - 1]), element.get_attribute("textContent"))
        else:
            print(counter, str(display_2[counter - 1]), element.get_attribute("textContent"))
        places_2.append(element.get_attribute("textContent"))
    counter = counter+1

print("\nRanking (special-departures-bridges):\n")

# float cast
new_prices_2 = []
for element in prices_2:
    rank = float(element)
    new_prices_2.append(rank)

# final list
list = dict(zip(places_2, new_prices_2))
ranking_2 = sorted(list.items(), key=operator.itemgetter(1))
for k, v in ranking_2:
    if v < 100.00:
        print("", "{0:.2f}".format(v), k)
    else:
        print("{0:.2f}".format(v), k)

# todo: sub-domain tracking 3
# access url
url_3 = "https://viajesloreto.com/viajes/"
browser.get(url_3)

# travel price scraper
display_3 = []
prices_3 = []
elements = browser.find_elements_by_css_selector('.package-info span.package-price')
for element in elements:
    price = element.get_attribute("textContent").strip('€')
    if len(price) == 6:
        price = " " + price
    if not ',' in price:
        price = price.strip(" ") + ",00 "
    display_3.append(price)
    price = price.replace(',', '.')
    prices_3.append(price)

print("\nDisplay (travels):\n")

# display (travels)
counter = 1
places_3 = []
elements = browser.find_elements_by_css_selector('.package-title-wrapper h2.package-title a')
for element in elements:
    if counter < 13:
        if counter < 10:
            print("", counter, str(display_3[counter - 1]), element.get_attribute("textContent"))
        else:
            print(counter, str(display_3[counter - 1]), element.get_attribute("textContent"))
        places_3.append(element.get_attribute("textContent"))
    counter = counter+1

print("\nRanking (travels):\n")

# float cast
new_prices_3 = []
for element in prices_3:
    rank = float(element)
    new_prices_3.append(rank)

# final list
list = dict(zip(places_3, new_prices_3))
ranking_3 = sorted(list.items(), key=operator.itemgetter(1))
for k, v in ranking_3:
    if v < 100.00:
        print("", "{0:.2f}".format(v), k)
    else:
        print("{0:.2f}".format(v), k)

# todo: sub-domain tracking 4
# access url
url_4 = "https://viajesloreto.com/excursiones/"
browser.get(url_4)

# excursion price scraper
display_4 = []
prices_4 = []
elements = browser.find_elements_by_css_selector('.package-info span.package-price')
for element in elements:
    price = element.get_attribute("textContent").strip('€')
    if len(price) == 6:
        price = " " + price
    if not ',' in price:
        price = price.strip(" ") + ",00 "
    display_4.append(price)
    price = price.replace(',', '.')
    prices_4.append(price)

print("\nDisplay (excursions):\n")

# display (excursions)
counter = 1
places_4 = []
elements = browser.find_elements_by_css_selector('.package-title-wrapper h2.package-title a')
for element in elements:
    if counter < 8:
        if counter < 10:
            print("", counter, str(display_4[counter - 1]), element.get_attribute("textContent"))
        else:
            print(counter, str(display_4[counter - 1]), element.get_attribute("textContent"))
        places_4.append(element.get_attribute("textContent"))
    counter = counter+1

print("\nRanking (excursions):\n")

# float cast
new_prices_4 = []
for element in prices_4:
    rank = float(element)
    new_prices_4.append(rank)

# final list
list = dict(zip(places_4, new_prices_4))
ranking_4 = sorted(list.items(), key=operator.itemgetter(1))
for k, v in ranking_4:
    if v < 100.00:
        print("", "{0:.2f}".format(v), k)
    else:
        print("{0:.2f}".format(v), k)



# close navigation session
time.sleep(2)
browser.quit()

# FIXME:
# homepage offers
# https://viajesloreto.com/
# special-departures-bridges
# https://viajesloreto.com/salidas-especiales-puentes/
# travels
# https://viajesloreto.com/viajes/
# excursions
# https://viajesloreto.com/excursiones/
# send report by email
