# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://www.nautaliaviajes.com/"


driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
driver.get(url)

inputElement = driver.find_element_by_id("hoteles_destino")
inputElement.clear()
inputElement.send_keys("london")

"""
inputElement = driver.find_element_by_id("hoteles_start_date")
inputElement.clear()
inputElement.send_keys("")
elementos = driver.find_elements_by_class_name("calendarCellOpen")
while True:

        if elementos:
            driver.find_element_by_class_name("calendarCellOpen").click()
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_acc_Calendario1_repFasce_ctl01_btnConferma").click() #confirm button
        else:

            driver.find_element_by_xpath("//input[@value='<']").click()  #back
            if elementos:
                driver.find_element_by_class_name("calendarCellOpen").click()
                driver.find_element_by_id("ctl00_ContentPlaceHolder1_acc_Calendario1_repFasce_ctl01_btnConferma").click()

            driver.find_element_by_xpath("//input[@value='>']").click() #forward
            if elementos:
                driver.find_element_by_class_name("calendarCellOpen").click()
                driver.find_element_by_id("ctl00_ContentPlaceHolder1_acc_Calendario1_repFasce_ctl01_btnConferma").click()

# inputElement.submit()

# element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((
#     By.XPATH,
#     '//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]'))).click()

# element = browser.find_element_by_xpath(
#     '//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]')
# element.clear()
# element.send_keys("London")
# element.click()
# TODO
# login_attempt = element.find_element_by_xpath("/html/body/form/div[1]/header/div[2]/div/div/div[2]/div[2]/button")
# login_attempt.click()

"""

# print(browser.current_url)  # TRACER
import time
time.sleep(20)
driver.quit()