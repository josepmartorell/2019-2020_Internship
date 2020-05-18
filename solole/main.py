import operator

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from xlsxwriter import Workbook
import os
import requests
import shutil


# driver version
# check = input("\nPress enter to check Selenium driver version...")
# os.system('python -c "import selenium; print(selenium.__version__)"')


# As you are using Selenium 3.8.0 you have to use GeckoDriver mandatory. But again as you are using Firefox v46.0 you
# have to set the capability marionette to False through DesiredCapabilities() as follows :
# REF:
# https://stackoverflow.com/questions/47782650/selenium-common-exceptions-sessionnotcreatedexception-message-unable
# -to-find-a/47785513

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False

class App:

    def __init__(self, username='BUSINESSTRAVEL', password='Trav567RT', target_city='new york',
                 path='/home/jmartorell/Booking'):  # Change this to your Target details and desired booking path
        self.username = username
        self.password = password
        self.target_city = target_city
        self.path = path
        # self.driver = webdriver.Firefox(capabilities=cap, executable_path='/usr/local/bin/geckodriver')  # Change
        # this to your FirefoxDriver path. todo: the expresion "executable_path=' was missed in the original version
        #  uncapable of locating the driver!!!!
        self.driver = webdriver.Firefox(
            executable_path='/usr/local/bin/geckodriver')  # Change this to your FirefoxDriver path.
        self.error = False
        self.timeout = 30
        self.main_url = 'https://b2b.solole.es'
        self.all_positions = []
        self.all_hotels = []
        self.all_addresses = []
        self.all_prices = []
        self.euro_symbol = '€'
        self.display = []
        self.cheap = []
        self.index = ""
        self.data = {}
        self.position = 0
        self.driver.get(self.main_url)
        sleep(1)
        self.log_in()
        if self.error is False:
            self.search_target_profile()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            self.file_manager()
        sleep(10)
        self.driver.close()

    def log_in(self, ):
        try:
            print('\nLogging in with username and password ...')
            user_name_input = self.driver.find_element_by_xpath('//input[@placeholder="Nombre de usuario"]')
            user_name_input.send_keys(self.username)
            sleep(1)

            password_input = self.driver.find_element_by_xpath('//input[@placeholder="Contraseña"]')
            password_input.send_keys(self.password)
            sleep(1)

            password_input.submit()
            sleep(1)

            # self.close_settings_window_if_there()
        except Exception:
            print('Some exception occurred while trying to find username or password field')
            self.error = True

    def search_target_profile(self):
        try:
            print("Manipulating search engine ...")
            search_bar = self.driver.find_element_by_xpath('//*[@id="hotelzonePred"]')
            search_bar.send_keys(self.target_city)
            # target_profile_url = self.main_url + '/' + self.target_city + '/'
            # self.driver.get(target_profile_url)
            sleep(1)
            # todo: accessing a drop-down menu item directly with xpath
            # element = self.driver.find_element_by_xpath('//iboosy-hotelzone/div[2]/div/button[2]/div')
            # element.click()
            # todo: accessing a drop-down menu item by position within the list
            #  https://selenium-python.readthedocs.io/navigating.html#interacting-with-the-page
            all_options = self.driver.find_elements_by_class_name('dropdown-item')
            all_options[0].click()
            sleep(1)

            self.driver.find_element_by_css_selector(
                'div.w-50:nth-child(1) > div:nth-child(2) > div:nth-child(1)').click()
            # todo: Within <div class = "ngb-dp-week ..."> the seven days of that week are stored each in a <div
            #  class = "ngb-dp-day ...">. Secondary click on the inspector on the day that interests you and copy the
            #  css selector, which you will use to click on in the calendar picker
            self.driver.find_element_by_css_selector('div.ngb-dp-month:nth-child(2) > '
                                                     'ngb-datepicker-month-view:nth-child(1) > div:nth-child(3) > '
                                                     'div:nth-child(1)').click()
            self.driver.find_element_by_css_selector('div.ngb-dp-month:nth-child(2) > '
                                                     'ngb-datepicker-month-view:nth-child(1) > div:nth-child(3) > '
                                                     'div:nth-child(7)').click()

            user_name_input = self.driver.find_element_by_xpath('//*[@id="nationalityPred"]')
            user_name_input.send_keys('espa')
            sleep(1)
            # todo: accessing a drop-down menu item directly with xpath
            element = self.driver.find_element_by_xpath(
                '//div[3]/iboosy-nationalities/div/div/ngb-typeahead-window/button/div/span[2]')
            element.click()
            login_button = self.driver.find_element_by_xpath('//*[@id="searchbtn"]')
            # instead of submit it works with click
            login_button.click()
            print('Loading page ...')
            sleep(1)

        except Exception:
            self.error = True
            print('Could not find search bar')

    def scroll_down(self):
        self.driver.implicitly_wait(20)

        try:
            # fixme: screen:
            no_of_pages = self.driver.find_element_by_xpath('//pagination-template/ul/li[9]/a/span[2]').text
            print("Quantity of pages: " + no_of_pages)

            no_of_results = self.driver.find_element_by_xpath(
                '//iboosy-accommodations-filter/div/div[1]/div[2]/h5').text
            no_of_results = no_of_results.replace(' RESULTADOS ENCONTRADOS', '')
            print("Quantity of results: " + no_of_results)

        except:
            pass

        try:
            # self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  # fixme: scroll
            # todo REF: https://stackoverflow.com/questions/48006078/how-to-scroll-down-in-python-selenium-step-by-step
            # FIXME 1: two ways to scroll down,
            #  1) go down to the bottom of the page at once.
            # self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  # fixme: scroll
            # FIXME 2:
            #  2) Descend from item to item to the bottom of the page.
            # in this example and item is the text of the button "See options":
            print('Scrolling page ...')
            read_mores = self.driver.find_elements_by_xpath('//div[text()="Precio desde"]')
            for read_more in read_mores:
                self.driver.execute_script("arguments[0].scrollIntoView();", read_more)
                # read_more.click()

            try:
                print("Scraping page ...")
                soup = BeautifulSoup(self.driver.page_source, 'lxml')  # todo: bs4
                hotel_list = soup.find_all('div', {'class': 'row result-option'})
                # fixme: name mechanism:
                for i, hotel in enumerate(hotel_list):
                    self.all_positions.append(i + 1)
                    hotel_name = hotel.find('span', {'_ngcontent-c18': ""}).getText()
                    hotel_name = ' '.join(hotel_name.split())
                    # print("%d - %s" % (i + 1, hotel_name))
                    self.all_hotels.append(hotel_name)
            except IOError as e:
                print("I/O error occurred: ", os.strerror(e.errno))
                print("Error loading the hotels ")
                pass

            try:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')  # todo: bs4
                address_list = soup.find_all('div', {'class': 'address'})
                # fixme: address mechanism:
                for i, address in enumerate(address_list):
                    hotel_address = address.find('span', {'_ngcontent-c18': ""}).getText()
                    hotel_address = ' '.join(hotel_address.split())
                    self.all_addresses.append(hotel_address)
            except IOError as e:
                print("I/O error occurred: ", os.strerror(e.errno))
                print("Error loading addresses ")
                pass

            try:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')  # todo: bs4
                price_list = soup.find_all('div', {'class': 'text-main-light prices'})
                # fixme: price mechanism:
                for i, price in enumerate(price_list):
                    hotel_price = price.find('span', {'_ngcontent-c18': ""}).getText().replace('€', '')
                    hotel_price = ' '.join(hotel_price.split())
                    if len(hotel_price) == 5:
                        hotel_price = "   " + hotel_price
                    if len(hotel_price) == 6:
                        hotel_price = "  " + hotel_price
                    if len(hotel_price) == 7:
                        hotel_price = " " + hotel_price
                    if len(hotel_price) == 8:
                        hotel_price = "" + hotel_price
                    self.all_prices.append(hotel_price)

            except IOError as e:
                print("I/O error occurred: ", os.strerror(e.errno))
                print("Error loading prices ")
                pass

            print("\n\tDisplay:\n")

            # display list
            list = zip(self.all_prices, self.all_hotels, self.all_addresses)
            for i, (j, k, v) in enumerate(list):
                if len(j) == 5:
                    j = "   " + j
                if len(j) == 6:
                    j = "  " + j
                if len(j) == 7:
                    j = " " + j
                if len(j) == 8:
                    j = "" + j
                if i < 9:
                    print(" %d - %s %s %s %s %s" % (i + 1, j, self.euro_symbol, k, " - ", v))
                else:
                    print("%d - %s %s %s %s %s" % (i + 1, j, self.euro_symbol, k, " - ", v))

            print("\n\tRanking:\n")

            # float cast
            new_prices = []
            for element in self.all_prices:
                rank = float(element)
                new_prices.append(rank)

            # fixme: final list
            # unlike in restel or bedsonline the following zip does not work with list (zip ())
            # display_list = list(zip(self.all_hotels, new_prices, self.all_addresses))
            display_list = zip(self.all_positions, self.all_hotels, new_prices, self.all_addresses)

            ranking = sorted(display_list, key=operator.itemgetter(2))
            for j, k, v, w in ranking:
                if v < 100.00:
                    print("   ", "{0:.2f}".format(v), k)
                if 99.00 < v < 1000.00:
                    print("  ", "{0:.2f}".format(v), k)
                if 999.00 < v < 10000.00:
                    print(" ", "{0:.2f}".format(v), k)
                if v > 9999.00:
                    print("", "{0:.2f}".format(v), k)

            self.cheap = ranking[0]
            self.data = ranking
            print('\nCheapest reservations: ', self.cheap[1], self.cheap[2], self.euro_symbol)
            self.display = display_list
            for i, collation in enumerate(display_list):
                if collation[1] == self.cheap[1]:
                    self.position = i
            print('Pointing to the target button ', self.position + 1, ' ...')
            # FIXME WARNING!!!! next line does not work with position -1 or just position! see it why...
            # Coincidentally, the first is the cheapest, that is, index 1, the variable self.index starts with 0,
            # therefore we must add 1. If we subtracted  -1 or we did not add anything, it was out of range,
            # and the spider did not I found the address.
            self.index = str(self.position + 1)
            if self.error is False:
                self.target_button(self.index)

        except NoSuchElementException:
            print('Some error occurred while trying to scroll down')
            self.error = True

    def target_button(self, index):
        target_button = self.driver.find_element_by_xpath(
            '//div[ ' + index + ' ]/div/div[1]/div[2]/div[2]/div[1]/div[2]/span')
        self.driver.execute_script("arguments[0].scrollIntoView();", target_button)
        # target_button.click()

    def file_manager(self, ):
        bookings_folder_path = os.path.join(self.path, 'bookings')
        if not os.path.exists(bookings_folder_path):
            os.mkdir(bookings_folder_path)
        # if self.error is False:
        #     self.write_bookings_to_excel_file(bookings_folder_path)
        # if self.error is False:
        #     self.read_bookings_from_excel_file(self.path + '/bookings/bookings.xlsx')


if __name__ == '__main__':
    app = App()
