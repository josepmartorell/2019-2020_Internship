from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
import os
import requests
import shutil


class App:
    def __init__(self, username='BUSINESS', password='459116RS', target_city='new york'):
        self.username = username
        self.password = password
        self.target_city = target_city
        self.driver = webdriver.Firefox(
            executable_path='/usr/local/bin/geckodriver')  # Change this to your FirefoxDriver path.
        self.error = False
        self.main_url = 'http://www.restel.es'
        self.all_hotels = []
        self.driver.get(self.main_url)
        sleep(1)
        self.log_in()
        if self.error is False:
            # self.close_dialog_box()
            # todo: REF:
            # https://es.stackoverflow.com/questions/109086/esperar-respuestas-para-continuar-selenium-python
            # The explicit wait, unlike an implicit one or what time.sleep does (although this is blocking)
            # however it was the solution for this search engine (compare with solole project where at this point sleep was useless)
            sleep(1) #### fixme: explicit wait
            self.search_target_profile()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            sleep(3)
        # self.driver.close()

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

    def search_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_css_selector('#filterHotels')
            search_bar.send_keys(self.target_city)
            # fixme: WARNING: immediately after entering the city in the field, in this case, we need an
            #  explicit wait of at least one second before clicking to display correctly the drop-down menu:
            sleep(1)
            search_bar.click()
            # enter destination city
            target_city = self.driver.find_element_by_css_selector(
                "li.item:nth-child(1) > div:nth-child(2) > span:nth-child(1)")
            target_city.click()
            sleep(1)
            # calendar picker
            self.driver.find_element_by_css_selector('#calendarHotels').click()
            sleep(1)
            # todo: accessing a drop-down calendar item by position within the list
            #  https://selenium-python.readthedocs.io/navigating.html#interacting-with-the-page
            all_options = self.driver.find_elements_by_class_name('available')
            all_options[0].click()
            all_options = self.driver.find_elements_by_class_name('available')
            all_options[6].click()
            sleep(2)
            # search button
            login_button = self.driver.find_element_by_xpath('//*[@id="search-hotels"]')
            # instead of submit it works with click
            login_button.click()
            sleep(3)
        except Exception:
            self.error = True
            print('Could not find search bar')

    def scroll_down(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        hotel_list = soup.find_all('a', {'class': 'hotel-name'})
        try:
            for i, hotel in enumerate(hotel_list):
                hotel_name = hotel.getText()
                self.all_hotels.append(hotel_name)
                print("%d - %s" % (i + 1, hotel_name))
            # print(self.all_hotels)

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

            sleep(2)
            # self.driver.close()
        except Exception as e:
            self.error = True
            print(e)
            print('Some error occurred while trying to scroll down')
        sleep(10)

    """
    def write_captions_to_excel_file(self, images, caption_path):
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
            pass
    """


if __name__ == '__main__':
    app = App()
