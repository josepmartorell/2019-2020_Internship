from telnetlib import EC

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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
    def __init__(self, username='BUSIN95C', password='020906Sm', target_username='paris',
                 path='/Users/Lazar/Desktop/bedsOnlineReport'):  # Change this to your search engine details and desired report path
        self.username = username
        self.password = password
        self.target_username = target_username
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
            sleep(4)  # fixme: implicit wait!
            # self.close_dialog_box()
            self.search_target_profile()
        # if self.error is False:
        #    self.scroll_down()
        # if self.error is False:
        #     if not os.path.exists(path):
        #         os.mkdir(path)
        #     self.downloading_images()
        # sleep(3)
        # self.driver.close()

    def log_in(self, ):
        try:
            # todo: dealing with popup windows
            # cookies popup
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/button[1]').click()
            # sleep(1)

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
                sleep(3)

                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
                    By.XPATH, '//*[@id="password"]')))
                password_input = self.driver.find_element_by_xpath('//*[@id="password"]')
                password_input.send_keys(self.password)
                sleep(1)

                user_name_input.submit()
                sleep(1)

                # self.close_settings_window_if_there()
            except Exception as e:
                print(e)
                self.error = True

    def search_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_xpath('//*[@id="s-destination-search"]')
            search_bar.send_keys(self.target_username).click()
            # target_profile_url = self.main_url + '/' + self.target_username + '/'
            # self.driver.get(target_profile_url)
            sleep(3)

        except Exception:
            self.error = True
            print('Could not find search bar')

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

    def scroll_down(self):
        try:
            no_of_posts = self.driver.find_element_by_xpath('//span[text()=" posts"]').text
            no_of_posts = no_of_posts.replace(' posts', '')
            no_of_posts = str(no_of_posts).replace(',', '')  # 15,483 --> 15483
            self.no_of_posts = int(no_of_posts)
            if self.no_of_posts > 12:
                no_of_scrolls = int(self.no_of_posts/12) + 3
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
            pass"""


if __name__ == '__main__':
    app = App()
