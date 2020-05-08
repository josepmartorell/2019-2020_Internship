import operator
from telnetlib import EC

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# todo: EXPECTED CONDITIONS https://selenium-python.readthedocs.io/waits.html
# https://stackoverflow.com/questions/58743549/attributeerror-bytes-object-has-no-attribute-element-to-be-clickable
# The import from telnetlib import EC. You need to import expected_conditions and use it as EC
# from selenium.webdriver.support import expected_conditions as EC...
from selenium.webdriver.support import expected_conditions as EC

from xlsxwriter import Workbook
import os
import requests
import shutil


class App:
    def __init__(self, username='BUSIN95C', password='020906Sm', target_continent='2', target_country_col='3',
                 target_country_row='1', target_city_col='4', target_city_row='94', path='//home/jmartorell/Booking'):
        self.username = username
        self.password = password
        self.target_continent = target_continent
        self.target_country_col = target_country_col
        self.target_country_row = target_country_row
        self.target_city_col = target_city_col
        self.target_city_row = target_city_row
        self.all_hotels = []
        self.all_prices = []
        self.path = path
        self.driver = webdriver.Firefox(
            executable_path="/usr/local/bin/geckodriver")  # Change this to your FirefoxDriver path.
        self.error = False
        self.main_url = 'https://www.bedsonline.com/home/es-es'
        self.all_images = []
        self.driver.get(self.main_url)
        sleep(1)
        self.log_in()
        if self.error is False:
            sleep(2)  # fixme: implicit wait!
            # self.close_dialog_box()
            self.search_target_profile()
        if self.error is False:
            self.scroll_down()
        # if self.error is False:
        #     if not os.path.exists(path):
        #         os.mkdir(path)
        #     self.file_manager()
        sleep(3)
        self.driver.close()

    def log_in(self, ):
        try:
            # todo: dealing with popup windows
            # cookies popup
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((
                By.XPATH,
                '//div/div/div[2]/button[1]'))).click()
            sleep(1)

        except Exception:
            self.error = True
            print('Unable to close popup window')
        else:
            try:
                # Press button to access the login fields
                sleep(1)
                login_button = self.driver.find_element_by_xpath(
                    '/html/body/div[2]/header/section[2]/div[1]/div/section[2]/a[1]')
                login_button.click()
                sleep(1)

                # todo: switch window
                #  https://sqa.stackexchange.com/questions/13792/how-to-proceed-after-clicking-a-link-to-new-page-in-selenium-in-python
                window_after = self.driver.window_handles[1]
                self.driver.switch_to.window(window_after)

                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
                    By.XPATH, '//*[@id="username"]')))
                user_name_input = self.driver.find_element_by_xpath('//*[@id="username"]')
                user_name_input.send_keys(self.username)
                sleep(1)

                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
                    By.XPATH, '//*[@id="password"]')))
                password_input = self.driver.find_element_by_xpath('//*[@id="password"]')
                password_input.send_keys(self.password)
                sleep(1)

                # user_name_input.submit()
                self.driver.find_element_by_xpath('//form/div[3]/button').submit()
                sleep(1)

            except Exception as e:
                print(e)
                self.error = True

    def search_target_profile(self):
        try:
            # todo: filling the search bar
            # search_bar.send_keys(self.target_username).click # this line is wrong, read below please
            # fixme: you cannot enter text directly use the autocomplete square icon to the right of the field
            WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((
                By.XPATH, '//section/div/form/fieldset[1]/div/a/span'))).click()
            sleep(2)

            # todo: https://dzone.com/articles/perform-actions-using-javascript-in-python-seleniu
            #  Method 1: Executing JavaScript at Document Root Level
            #  javaScript = "document.getElementsByClassName('ui-dialog-titlebar-close ui-corner-all')[0].click();"
            #  self.driver.execute_script(javaScript)
            #  Method 2: Executing JavaScript at Element Level:

            try:
                wait = WebDriverWait(self.driver, 100)
                wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#continent-picker-tab > li:nth-child"
                                          "(" + self.target_continent + ") > a:nth-child(1)")))
                print("Manipulating search engine ...")
            except TimeoutException:
                print("Searching took too much time!")

            if self.target_continent != '4':
                picker = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    "#continent-picker-tab > li:nth-child(" + self.target_continent + ") > a:nth-child(1)")))
                self.driver.execute_script("arguments[0].click();", picker)
                sleep(1)
            picker = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((
                By.XPATH,
                "//section/article[1]/div/ul[" + self.target_country_col + "]/li[" + self.target_country_row + "]/a")))
            self.driver.execute_script("arguments[0].click();", picker)
            sleep(1)
            picker = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((
                By.XPATH,
                "//section/article[2]/div/ul[" + self.target_city_col + "]/li[" + self.target_city_row + "]/a")))
            self.driver.execute_script("arguments[0].click();", picker)
            sleep(1)
            picker = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((
                By.XPATH,
                "//article[3]/div/ul[1]/li[1]/a")))
            self.driver.execute_script("arguments[0].click();", picker)
            sleep(1)

            # search button
            login_button = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="mainsearch"]')))
            login_button.submit()

        except Exception:
            self.error = True
            print('Could not find search bar')

    def scroll_down(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#form-cheapest-acc-hot13445 > button:nth-child(1)')))
            print("Waiting ajax full load ...")

        except TimeoutException:
            print("Loading took too much time!")

        try:
            # self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            read_mores = self.driver.find_elements_by_xpath('//form/button')
            for read_more in read_mores:
                self.driver.execute_script("arguments[0].scrollIntoView();", read_more)
                # read_more.click()
            sleep(1)

            # even 25 seconds may not be enough to load the page!
            # todo AJAX: maximum 30 seconds
            sleep(11)  # wait ajax full load

            print("Scraping page ...")
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            hotel_list = soup.find_all('article', {'class': 'crosselling-line availability-item'})
            euro_symbol = '€'
            print("\n\tDisplay:\n")
            try:
                for i, hotel in enumerate(hotel_list):
                    hotel_name = hotel.find('a', {'data-tl': 'acc-title'}).getText()
                    # fixme: remove whitespaces REF: https://stackoverrun.com/es/q/743639
                    hotel_name = ' '.join(hotel_name.split())
                    self.all_hotels.append(hotel_name)
                    # print(" %d - %s" % (i + 1, hotel_name))

                    hotel_integer = hotel.find('span', {'class': 'hotel-price'}).getText()
                    hotel_decimal = hotel.find('span', {'class': 'hotel-price-decimal'}).getText().strip('€')
                    hotel_integer = hotel_integer.replace(',', '')
                    hotel_price = '{}.{}'.format(hotel_integer, hotel_decimal)
                    hotel_price = float(hotel_price)
                    hotel_price = "{0:.2f}".format(hotel_price)
                    self.all_prices.append(hotel_price)
                    if len(hotel_price) == 5:
                        hotel_price = "   " + hotel_price
                    if len(hotel_price) == 6:
                        hotel_price = "  " + hotel_price
                    if len(hotel_price) == 7:
                        hotel_price = " " + hotel_price
                    if len(hotel_price) == 8:
                        hotel_price = "" + hotel_price

                    if i < 9:
                        print(" %d - %s %s %s" % (i + 1, hotel_price, euro_symbol, hotel_name))
                    else:
                        print("%d - %s %s %s" % (i + 1, hotel_price, euro_symbol, hotel_name))

                print("\n\tRanking:\n")
                # float cast
                new_prices_2 = []
                for element in self.all_prices:
                    rank = float(element)
                    new_prices_2.append(rank)

                # final list
                list = dict(zip(self.all_hotels, new_prices_2))
                ranking_2 = sorted(list.items(), key=operator.itemgetter(1))
                for k, v in ranking_2:
                    if v < 100.00:
                        print("   ", "{0:.2f}".format(v), k)
                    if 99.00 < v < 1000.00:
                        print("  ", "{0:.2f}".format(v), k)
                    if 999.00 < v < 10000.00:
                        print(" ", "{0:.2f}".format(v), k)
                    if v > 9999.00:
                        print("", "{0:.2f}".format(v), k)

                sleep(2)
            except Exception as e:
                self.error = True
                print(e)
                print('Some error occurred while trying to scratch the hotel list')

            # activate page analyzer
            input('\nBREAK: \n\tActivate the analyzer?')
            print(soup.prettify())

        except NoSuchElementException:
            print('Some error occurred while trying to scroll down')
            self.error = True

    """def write_captions_to_excel_file(self, images, caption_path):
        print('writing to excel')
        workbook = Workbook(os.path.join(caption_path, 'captions.xlsx'))
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0, 'Image name')       # 3 --> row number, column number, value
        worksheet.write(row, 1, 'Caption')
        row += 1
        for index, image in enumerate(images):
            filename = 'image_' + str(index) + '.jpg'
            try:
                caption = image['alt']
            except KeyError:
                caption = 'No caption exists'
            worksheet.write(row, 0, filename)
            worksheet.write(row, 1, caption)
            row += 1
        workbook.close()

    def download_captions(self, images):
        captions_folder_path = os.path.join(self.path, 'captions')
        if not os.path.exists(captions_folder_path):
            os.mkdir(captions_folder_path)
        self.write_captions_to_excel_file(images, captions_folder_path)
        '''for index, image in enumerate(images):
            try:
                caption = image['alt']
            except KeyError:
                caption = 'No caption exists for this image'
            file_name = 'caption_' + str(index) + '.txt'
            file_path = os.path.join(captions_folder_path, file_name)
            link = image['src']
            with open(file_path, 'wb') as file:
                file.write(str('link:' + str(link) + '\n' + 'caption:' + caption).encode())'''


    def downloading_images(self):
        self.all_images = list(set(self.all_images))
        self.download_captions(self.all_images)
        print('Length of all images', len(self.all_images))
        for index, image in enumerate(self.all_images):
            filename = 'image_' + str(index) + '.jpg'
            image_path = os.path.join(self.path, filename)
            link = image['src']
            print('Downloading image', index)
            response = requests.get(link, stream=True)
            try:
                with open(image_path, 'wb') as file:
                    shutil.copyfileobj(response.raw, file)  # source -  destination
            except Exception as e:
                print(e)
                print('Could not download image number ', index)
                print('Image link -->', link)

    def close_dialog_box(self):
        # reload page
        sleep(2)
        self.driver.get(self.driver.current_url)
        sleep(3)

        try:
            sleep(3)
            not_now_btn = self.driver.find_element_by_xpath('//*[text()="Not Now"]')
            sleep(3)

            not_now_btn.click()
            sleep(1)
        except Exception:
            pass


    def close_settings_window_if_there(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as e:
            pass"""


if __name__ == '__main__':
    app = App()
