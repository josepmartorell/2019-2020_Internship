# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TODO: screen all steps to control the process...

# driver version
check = input("\nPress enter to check Selenium driver version...")
os.system('python -c "import selenium; print(selenium.__version__)"')

# url access
url = "https://www.nautaliaviajes.com/"
driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
driver.get(url)
assert "NAUTALIA VIAJES" in driver.title
currentTime = datetime.datetime.now()
print("\nSITE ", driver.current_url, "\nDATE ", currentTime)

# todo: method to catch elements that need time to be load to be visible...

var_id = By.ID
var_name = By.NAME
var_class = By.CLASS_NAME
var_link = By.LINK_TEXT
var_xpath = By.XPATH
var_css = By.CSS_SELECTOR


def element_wait(var_selected, route, wait=6):
    try:
        WebDriverWait(driver, wait, 1).until(EC.presence_of_element_located((var_selected, route)))
    except:
        raise NameError("Please enter the  elements,"
                        "'var_id',"
                        "'var_name',"
                        "'var_class',"
                        "'var_link',"
                        "'var_xpath',"
                        "'var_css'."
                        )


# todo: crossing the search engine...

# dealing with popup windows
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="id_boton_cerrar_aviso_pc"]').click()
element_wait(var_xpath, '//*[@id="onesignal-popover-cancel-button"]')
driver.find_element_by_xpath('//*[@id="onesignal-popover-cancel-button"]').click()

well_come_window = element_wait(var_xpath, "/html/body/div[7]/div/span")
# well_come_window.click()

try:
    alert = driver.switch_to.alert()
    print(alert.text)
    alert.accept()
except:
    print("no alert to accept")

javaScript = "document.getElementsByClassName('close-modal')[0].click();"
driver.execute_script(javaScript)

# search box
element_wait(var_id, 'hoteles_destino')
element = driver.find_element_by_id('hoteles_destino')
element.clear()
element.send_keys("Almaty", Keys.ARROW_DOWN)

actions = ActionChains(driver)
for _ in range(0):
    actions.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1)

javaScript = "document.getElementsByClassName('close-modal')[0].click();"
driver.execute_script(javaScript)

driver.find_element_by_xpath('/html/body/ul/li/a/table/tbody/tr/td[2]/strong').click()
driver.find_element_by_xpath('//*[@id="hoteles_start_date"]').click()
driver.find_element_by_xpath('//table/tbody/tr[4]/td[1]/a').click()
driver.find_element_by_xpath('//*[@id="btnSend"]').click()


# close navigation session
time.sleep(10)
# driver.quit()

# FIXME:
# https://unipython.com/navegando-con-selenium/
# https://dzone.com/articles/perform-actions-using-javascript-in-python-seleniu
