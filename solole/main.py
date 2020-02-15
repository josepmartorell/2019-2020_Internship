from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
import os
import requests
import shutil

# driver version
check = input("\nPress enter to check Selenium driver version...")
os.system('python -c "import selenium; print(selenium.__version__)"')


# As you are using Selenium 3.8.0 you have to use GeckoDriver mandatory. But again as you are using Firefox v46.0 you
# have to set the capability marionette to False through DesiredCapabilities() as follows :
# REF:
# https://stackoverflow.com/questions/47782650/selenium-common-exceptions-sessionnotcreatedexception-message-unable
# -to-find-a/47785513

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False

class App:
    def __init__(self, username='BUSINESSANDTRAVEL', password='Trav567RT', target_username='datafinder2016',
                 path='/home/jmartorell/Imágenes/sololePhotos'):  # Change this to your Target details and desired images path
        self.username = username
        self.password = password
        self.target_username = target_username
        self.path = path
        # self.driver = webdriver.Firefox(capabilities=cap, executable_path='/usr/local/bin/geckodriver')  # Change
        # this to your FirefoxDriver path. todo: the expresion "executable_path=' was missed in the original version
        #  uncapable of locating the driver!!!!
        self.driver = webdriver.Firefox(
            executable_path='/usr/local/bin/geckodriver')  # Change this to your FirefoxDriver path.
        self.error = False
        self.main_url = 'https://www.solole.es/'
        self.all_images = []
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        if self.error is False:
            self.close_dialog_box()
            self.open_target_profile()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            self.downloading_images()
        sleep(3)
        self.driver.close()

    def log_in(self, ):
        try:
            log_in_button = self.driver.find_element_by_class_name('slide-btn')
            log_in_button.click()
            sleep(3)
        except Exception:
            self.error = True
            print('Unable to find login button')
        else:
            try:
                user_name_input = self.driver.find_element_by_xpath('//input[@placeholder="Nombre de usuario"]')
                user_name_input.send_keys(self.username)
                sleep(1)

                password_input = self.driver.find_element_by_xpath('//input[@placeholder="Contraseña"]')
                password_input.send_keys(self.password)
                sleep(1)

                #user_name_input.submit()
                #sleep(1)

                #self.close_settings_window_if_there()
            except Exception:
                print('Some exception occurred while trying to find username or password field')
                self.error = True

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

    def open_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_xpath('//input[@placeholder="Search"]')
            search_bar.send_keys(self.target_username)
            target_profile_url = self.main_url + '/' + self.target_username + '/'
            self.driver.get(target_profile_url)
            sleep(3)
        except Exception:
            self.error = True
            print('Could not find search bar')

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


if __name__ == '__main__':
    app = App()
