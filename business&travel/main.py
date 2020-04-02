# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class App:
    def __init__(self, username='business.travel', password='Busi2016', target_destination='tokio',
                 path='/home/jmartorell/Imágenes/business&travelPhotos'):
        self.username = username
        self.password = password
        self.target_destination = target_destination
        self.path = path
        self.browser = webdriver.Firefox(
            executable_path='/usr/local/bin/geckodriver')
        self.error = False
        self.url = 'https://pro.w2m.travel'
        self.all_images = []
        self.browser.get(self.url)
        sleep(1)
        self.log_in()
        if self.error is False:
            # self.close_dialog_box()
            self.search_engine_insert()
        '''if self.error is False:
            self.scroll_down()'''
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            self.reach_target()
        # close the browser
        sleep(6)
        self.browser.quit()

    def log_in(self, ):
        try:
            input_element = self.browser.find_element_by_id("email")
            input_element.clear()
            input_element.send_keys("business.travel")
            input_element = self.browser.find_element_by_id("password")
            input_element.clear()
            input_element.send_keys("Busi2016")
            input_element.submit()
        except Exception:
            print('Some exception occurred while trying to find username or password field')
            self.error = True

    def search_engine_insert(self):
        # wait to load the search engine
        element = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((
            By.XPATH,
            '//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]'))).click()
        element = self.browser.find_element_by_xpath(
            '//*[@id="hotel-searcher-_ctl1__ctl1__ctl1_pageBody_pageBody_searcher__ctl0_ctlZoneSelector-input"]')
        element.clear()

        # check access
        assert "Hoteles | W2M" in self.browser.title
        print(self.browser.current_url)

        # enter data in input field
        element.send_keys(self.target_destination)

        # TODO:
        # drop-down item selection
        actions = ActionChains(self.browser)
        for _ in range(3):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(1)

        # enter destination city
        target_city = element.find_element_by_xpath(
            "//header/div[2]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/span[2]/div/div[3]/div[5]")
        target_city.click()

        # press the search button
        login_attempt = element.find_element_by_xpath(
            "/html/body/form/div[1]/header/div[2]/div/div/div[2]/div[2]/button")
        login_attempt.click()

    def reach_target(self):
        element = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((
            By.XPATH,
            '//main/div[1]/div/div[1]/article/div[1]/div[2]/h2'))).click()


if __name__ == '__main__':
    app = App()

# FIXME: descending design
# 1) init method initializes variables that will be accessible by self from any method of the class
# 2) log in method allows us to log in to access the provider's services
# 3) search engine insert method fills in the search engine fields and clicks on the search button
# 4) the reach target method systematically selects the first objective by clicking on it
