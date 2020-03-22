from telnetlib import EC

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

from selenium.common.exceptions import TimeoutException
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
    def __init__(self, username='BUSINESSTRAVEL', password='Trav567RT', target_city='London',
                 path='/home/jmartorell/Imágenes/sololePhotos'):  # Change this to your Target details and desired images path
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
        self.all_images = []
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        if self.error is False:
            # self.close_dialog_box()
            self.search_target_profile()
        # if self.error is False:
            # self.scroll_down()
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            # self.downloading_images()
        sleep(3)
        # self.driver.close()

    def log_in(self, ):

        try:
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
            search_bar = self.driver.find_element_by_xpath('//*[@id="hotelzonePred"]')
            search_bar.send_keys(self.target_city)
            # target_profile_url = self.main_url + '/' + self.target_city + '/'
            # self.driver.get(target_profile_url)
            sleep(3)
            # todo: accessing a drop-down menu item directly with xpath
            # element = self.driver.find_element_by_xpath('//iboosy-hotelzone/div[2]/div/button[2]/div')
            # element.click()
            # todo: accessing a drop-down menu item by position within the list
            #  https://selenium-python.readthedocs.io/navigating.html#interacting-with-the-page
            all_options = self.driver.find_elements_by_class_name('dropdown-item')
            all_options[1].click()
            sleep(1)

            self.driver.find_element_by_css_selector('div.w-50:nth-child(1) > div:nth-child(2) > div:nth-child(1)').click()
            # todo: Within <div class = "ngb-dp-week ..."> the seven days of that week are stored each in a <div
            #  class = "ngb-dp-day ...">. Secondary click on the inspector on the day that interests you and copy the
            #  css selector, which you will use to click on in the calendar picker
            self.driver.find_element_by_css_selector('div.ngb-dp-month:nth-child(2) > '
                                                     'ngb-datepicker-month-view:nth-child(1) > div:nth-child(3) > '
                                                     'div:nth-child(1)').click()
            self.driver.find_element_by_css_selector('div.ngb-dp-month:nth-child(2) > '
                                                     'ngb-datepicker-month-view:nth-child(1) > div:nth-child(3) > '
                                                     'div:nth-child(7)').click()
            # self.driver.find_element_by_css_selector('').click()

            user_name_input = self.driver.find_element_by_xpath('//*[@id="nationalityPred"]')
            user_name_input.send_keys('espa')
            sleep(2)
            # todo: accessing a drop-down menu item directly with xpath
            element = self.driver.find_element_by_xpath('/html/body/iboosy-app/div/div/ng-component/div/div[2]/div['
                                                        '2]/iboosy-accommodations-search/div[1]/div/div/div['
                                                        '3]/iboosy-nationalities/div/div/ngb-typeahead-window/button'
                                                        '/div/span[2]')
            element.click()
            login_button = self.driver.find_element_by_xpath('//*[@id="searchbtn"]')
            # instead of submit it works with click
            login_button.click()
            sleep(3)

        except Exception:
            self.error = True
            print('Could not find search bar')

    """
    def write_captions_to_excel_file(self, images, caption_path):
        print('writing to excel')
        workbook = Workbook(os.path.join(caption_path, 'captions.xlsx'))
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0, 'Image name')  # 3 --> row number, column number, value
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

    def scroll_down(self):
        try:
            no_of_posts = self.driver.find_element_by_xpath('//span[text()=" posts"]').text
            no_of_posts = no_of_posts.replace(' posts', '')
            no_of_posts = str(no_of_posts).replace(',', '')  # 15,483 --> 15483
            self.no_of_posts = int(no_of_posts)
            if self.no_of_posts > 12:
                no_of_scrolls = int(self.no_of_posts / 12) + 3
                try:
                    for value in range(no_of_scrolls):
                        soup = BeautifulSoup(self.driver.page_source, 'lxml')
                        for image in soup.find_all('img'):
                            self.all_images.append(image)
                        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        sleep(2)
                except Exception as e:
                    self.error = True
                    print(e)
                    print('Some error occurred while trying to scroll down')
            sleep(10)
        except Exception:
            print('Could not find no of posts while trying to scroll down')
            self.error = True

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
