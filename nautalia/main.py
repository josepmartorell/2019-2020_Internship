# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
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
print("\nSITE ",driver.current_url,  "\nDATE ",currentTime)

# todo: insert variables VAR1,VAR2 to catch elements that need to be visible in this method...

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
driver.find_element_by_xpath('//*[@id="id_boton_cerrar_aviso_pc"]').click()
driver.find_element_by_xpath('//*[@id="onesignal-popover-cancel-button"]').click()

# todo: driver.find_element_by_xpath('/html/body/div[7]/div/span').click()
# raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.NoSuchElementException:
# Message: Unable to locate element: /html/body/div[7]/div/span
# todo: driver.find_element_by_class_name('close-modal').click()
# raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: .close-modal

# driver.find_element_by_xpath('').click()
# driver.find_element_by_xpath('').click()
# driver.find_element_by_xpath('').click()
# driver.find_element_by_xpath('').click()


# close navigation session
time.sleep(10)
driver.quit()

# FIXME:
# https://programacion.net/articulo/10_consejos_y_trucos_avanzados_de_webdriver_1319 review
# python-selenium/util/selse_feng.py set visible elements function
# .py", line 242, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: /html/body/div[7]/div/span