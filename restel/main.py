import datetime
import operator

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
import os
import requests
import shutil


class App:
    def __init__(self, username='BUSINESS', password='459116RS', target_city='new york', stay=7,
                 path='//home/jmartorell/Booking'):
        self.username = username
        self.password = password
        self.target_city = target_city
        self.stay = stay
        self.path = path
        self.driver = webdriver.Firefox(
            executable_path='/usr/local/bin/geckodriver')  # Change this to your FirefoxDriver path.
        self.error = False
        self.main_url = 'http://www.restel.es'
        self.all_hotels = []
        self.all_prices = []
        self.all_addresses = []
        self.display = []
        self.cheap = []
        self.index = ""
        self.driver.get(self.main_url)
        sleep(1)
        self.log_in()
        if self.error is False:
            # self.close_dialog_box()
            # todo: REF:
            #  https://es.stackoverflow.com/questions/109086/esperar-respuestas-para-continuar-selenium-python
            # The explicit wait, unlike an implicit one or what time.sleep does (although this is blocking)
            # however it was the solution for this search engine (compare with solole project where at this
            # point sleep was useless)
            sleep(1)  #### fixme: explicit wait
            self.search_target_profile()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            self.target_button(self.index)
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            self.file_manager()
        sleep(1)
        self.driver.close()

    def log_in(self, ):
        try:
            # fixme: the xpath did not work selected with the right mouse button (neither with the css selector). The
            #  solution has been to use the variable "placeholder" as xpath, taking it from the same script used in
            #  solole.
            user_name_input = self.driver.find_element_by_xpath('//input[@placeholder="Usuario"]')
            user_name_input.send_keys(self.username)
            sleep(1)

            password_input = self.driver.find_element_by_xpath('//input[@placeholder="Contraseña"]')
            password_input.send_keys(self.password)
            sleep(1)

            user_name_input.submit()
            sleep(1)

            # self.close_settings_window_if_there()
        except Exception:
            print('Some exception occurred while trying to find username or password field')
            self.error = True

    def flip_calendar(self, days):
        today = datetime.datetime.utcnow()
        print("CHECK IN:  ", today)
        check_out = today + datetime.timedelta(days)
        print("CHECK OUT: ", check_out)

        flip = check_out.month - today.month
        return flip

    def search_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_css_selector('#filterHotels')
            search_bar.send_keys(self.target_city)
            # fixme: WARNING: immediately after entering the city in the field, in this case, we need an
            #  explicit wait of at least one second before clicking to display correctly the drop-down menu:
            sleep(2)
            search_bar.click()
            # enter destination city
            target_city = self.driver.find_element_by_css_selector(
                "li.item:nth-child(1) > div:nth-child(2) > span:nth-child(1)")
            target_city.click()
            sleep(1)

            # calendar picker
            self.driver.find_element_by_css_selector('#calendarHotels').click()
            sleep(1)
            if self.flip_calendar(self.stay) == 0:
                # todo: accessing a drop-down calendar item by position within the list
                #  https://selenium-python.readthedocs.io/navigating.html#interacting-with-the-page
                all_options = self.driver.find_elements_by_class_name('available')
                all_options[0].click()
                all_options = self.driver.find_elements_by_class_name('available')
                all_options[self.stay - 1].click()
                sleep(2)
            else:
                all_options = self.driver.find_elements_by_class_name('available')
                all_options[0].click()
                self.driver.find_element_by_css_selector('div.drp-calendar:nth-child(3)').click()

            # search button
            login_button = self.driver.find_element_by_xpath('//*[@id="search-hotels"]')
            # instead of submit it works with click
            login_button.click()
            sleep(3)
        except Exception:
            self.error = True
            print('Could not find search bar')

    def scroll_down(self):
        global position
        self.driver.implicitly_wait(20)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        hotel_list = soup.find_all('div', {'class': 'element'})
        euro_symbol = '€'

        # todo REF: https://stackoverflow.com/questions/48006078/how-to-scroll-down-in-python-selenium-step-by-step
        # FIXME 1: two ways to scroll down,
        #  1) go down to the bottom of the page at once.
        # self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        # FIXME 2:
        #  2) Descend from item to item to the bottom of the page.
        # in this example and item is the text of the button "See options":
        read_mores = self.driver.find_elements_by_xpath('//a[text()="Ver opciones"]')
        for read_more in read_mores:
            self.driver.execute_script("arguments[0].scrollIntoView();", read_more)
            # read_more.click()

        print("\n\tdisplay:\n")
        try:
            for i, hotel in enumerate(hotel_list):

                hotel_price = hotel.find('span', {'class': 'final-price'}).getText().strip('€')
                hotel_price = hotel_price.replace('.', '')
                hotel_price = hotel_price.replace(',', '.')
                hotel_price = float(hotel_price)
                hotel_price = "{0:.2f}".format(hotel_price)
                self.all_prices.append(hotel_price)
                if len(hotel_price) == 5:
                    hotel_price = "   " + hotel_price
                if len(hotel_price) == 6:
                    hotel_price = "  " + hotel_price
                if len(hotel_price) == 7:
                    hotel_price = " " + hotel_price

                hotel_name = hotel.find('a', {'class': 'hotel-name'}).getText()
                hotel_address = hotel.find('span', {'class': 'address-content'}).getText()
                self.all_hotels.append(hotel_name)
                self.all_addresses.append(hotel_address)
                if i < 9:
                    print(" %d - %s %s %s - %s" % (i + 1, hotel_price, euro_symbol, hotel_name, hotel_address))
                else:
                    print("%d - %s %s %s - %s" % (i + 1, hotel_price, euro_symbol, hotel_name, hotel_address))
            print("\n\tranking:\n")

            # float cast
            new_prices_2 = []
            for element in self.all_prices:
                rank = float(element)
                new_prices_2.append(rank)

            # final list
            # dict version allow just 2 values 'k' and 'v':
            # list = dict(zip(self.all_hotels, new_prices_2))
            # ranking_2 = sorted(list.items(), key=operator.itemgetter(1))
            # for k, v in ranking_2:...etc'''
            # with common zip package we easily pack the addresses too:
            display_list = list(zip(self.all_hotels, new_prices_2, self.all_addresses))
            ranking_2 = sorted(display_list, key=operator.itemgetter(1))
            # todo REF: https://discuss.codecademy.com/t/how-can-i-sort-a-zipped-object/454412/6
            for k, v, w in ranking_2:
                if v < 100.00:
                    print("   ", "{0:.2f}".format(v), k, "-", w)
                if 99.00 < v < 1000.00:
                    print("  ", "{0:.2f}".format(v), k, "-", w)
                if 999.00 < v < 10000.00:
                    print(" ", "{0:.2f}".format(v), k, "-", w)
                if v > 9999.00:
                    print("", "{0:.2f}".format(v), k, "-", w)

            self.cheap = ranking_2[0]
            print('\nCheapest reservations: ', self.cheap[0], self.cheap[1], euro_symbol)
            # self.display = display_list[7]
            # print('Target button number: ', self.display.index(self.cheap[0]))
            self.display = display_list
            for i, collation in enumerate(display_list):
                if collation[0] == self.cheap[0]:
                    position = i
            print('Position of the target button: ', position + 1)
            self.index = str(position - 1)

            sleep(2)
        except Exception as e:
            self.error = True
            print(e)
            print('Some error occurred while trying to scroll down')

    def target_button(self, index):
        target_button = self.driver.find_element_by_xpath(
            '//app-search-results-list/div/div[1]/div/div[1]/div[' + index + ']/div/div[3]/div/div[3]/a')
        self.driver.execute_script("arguments[0].scrollIntoView();", target_button)
        # target_button.click()

    def file_manager(self, ):
        bookings_folder_path = os.path.join(self.path, 'bookings')
        if not os.path.exists(bookings_folder_path):
            os.mkdir(bookings_folder_path)
        if self.error is False:
            self.write_bookings_to_excel_file(bookings_folder_path)

        billing_folder_path = os.path.join(self.path, 'billing')
        if not os.path.exists(billing_folder_path):
            os.mkdir(billing_folder_path)
        # self.write_captions_to_excel_file(images, captions_folder_path)

    def write_bookings_to_excel_file(self, booking_path):
        print('\nwriting the reservation at the hotel ' + self.cheap[0] + ' to excel file...')
        workbook = Workbook(os.path.join(booking_path, 'bookings.xlsx'))
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0, 'Code')       # 3 --> row number, column number, value
        worksheet.write(row, 1, 'Price')
        worksheet.write(row, 2, 'Hotel')
        worksheet.write(row, 3, 'Address')

        row += 1

        worksheet.write(row, 0, 'AA00')
        worksheet.write(row, 1, self.cheap[1])
        worksheet.write(row, 2, self.cheap[0])
        worksheet.write(row, 3, self.cheap[2])
        row += 1
        workbook.close()


if __name__ == '__main__':
    app = App()
