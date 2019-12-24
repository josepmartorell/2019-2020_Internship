# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# url access
url = "https://www.nautaliaviajes.com/"
driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
driver.get(url)

# page checking
assert "NAUTALIA VIAJES" in driver.title
print(driver.current_url)


# cookies policy alert
alert = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
    By.ID,
    'capaAvisoPoliticaCookies_superior_mensajes')))
alert.click()

# enter data in input field
input = driver.find_element_by_xpath(
    '//*[@id="hoteles_destino"]')
input.clear()
input.send_keys("london")


# close navigation session
time.sleep(10)
driver.quit()

# FIXME:
# raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.ElementClickInterceptedException:
# Message: Element <input id="hoteles_destino" class="frnv-input ui-autocomplete-input"
# name="hoteles_destino" type="text"> is not clickable at point (206,613)
# because another element <div id="capaAvisoPoliticaCookies_superior_mensajes"
# class="capaAvisoPoliticaCookies_superior_mensajes"> obscures it
