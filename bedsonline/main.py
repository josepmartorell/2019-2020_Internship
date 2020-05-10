import operator
from time import sleep
from telnetlib import EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
# todo: EXPECTED CONDITIONS https://selenium-python.readthedocs.io/waits.html
# https://stackoverflow.com/questions/58743549/attributeerror-bytes-object-has-no-attribute-element-to-be-clickable
# The import from telnetlib import EC. You need to import expected_conditions and use it as EC
# from selenium.webdriver.support import expected_conditions as EC...
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
from openpyxl import Workbook
import requests
import os


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
        self.all_zones = []
        self.display = []
        self.cheap = []
        self.index = ""
        self.data = {}
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
            # todo: dealing with popup windows
            # cookies popup
            print('Closing cookies window ...')
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
                    '//section[2]/div[1]/div/section[2]/a[1]')
                login_button.click()
                sleep(1)

                # todo: switch window
                #  https://sqa.stackexchange.com/questions/13792/how-to-proceed-after-clicking-a-link-to-new-page-in-selenium-in-python
                window_after = self.driver.window_handles[1]
                self.driver.switch_to.window(window_after)
                print('Logging in with username and password ...')

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

            # todo: https://dzone.com/articles/perform-actions-using-javascript-in-python-seleniu
            #  Method 1: Executing JavaScript at Document Root Level
            #  javaScript = "document.getElementsByClassName('ui-dialog-titlebar-close ui-corner-all')[0].click();"
            #  self.driver.execute_script(javaScript)
            #  Method 2: Executing JavaScript at Element Level:
            print("Manipulating search engine ...")
            try:
                wait = WebDriverWait(self.driver, 100)
                wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#continent-picker-tab > li:nth-child"
                                          "(" + self.target_continent + ") > a:nth-child(1)")))
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
            print('Loading page ...')
            login_button.submit()

        except Exception:
            self.error = True
            print('Could not find search bar')

    def scroll_down(self):
        global position
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#form-cheapest-acc-hot13445 > button:nth-child(1)')))

        except TimeoutException:
            print("Loading took too much time!")

        try:
            print('Scrolling page ...')
            # self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            read_mores = self.driver.find_elements_by_xpath('//form/button')
            for read_more in read_mores:
                self.driver.execute_script("arguments[0].scrollIntoView();", read_more)
                # read_more.click()
            sleep(1)

            # even 25 seconds may not be enough to load the page!
            # todo AJAX: maximum 30 seconds
            print('Waiting ajax full load ...')
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

                    hotel_zone = hotel.find('span', {'class': '_hotelzone'}).getText()
                    hotel_name = ' '.join(hotel_name.split())
                    self.all_zones.append(hotel_zone)

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
                        print(" %d - %s %s %s - %s" % (i + 1, hotel_price, euro_symbol, hotel_name, hotel_zone))
                    else:
                        print("%d - %s %s %s - %s" % (i + 1, hotel_price, euro_symbol, hotel_name, hotel_zone))

                print("\n\tRanking:\n")
                # float cast
                new_prices = []
                for element in self.all_prices:
                    rank = float(element)
                    new_prices.append(rank)

                # final list
                display_list = list(zip(self.all_hotels, new_prices, self.all_zones))
                ranking = sorted(display_list, key=operator.itemgetter(1))
                # todo REF: https://discuss.codecademy.com/t/how-can-i-sort-a-zipped-object/454412/6
                for k, v, w in ranking:
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
                print('\nCheapest reservation: ', self.cheap[0], self.cheap[1], euro_symbol)
                # self.display = display_list[7]
                # print('Target button number: ', self.display.index(self.cheap[0]))
                self.display = display_list
                for i, collation in enumerate(display_list):
                    if collation[0] == self.cheap[0]:
                        position = i
                print('Pointing to the target button ', position + 1, ' ...')
                self.index = str(position)
                if self.error is False:
                    self.target_button(self.index)

                sleep(2)
            except Exception as e:
                self.error = True
                print(e)
                print('Some error occurred while trying to scratch the hotel list')

            # activate page analyzer
            print('Downloading html to computer ...')
            file = open("bedsonline.html", "w")
            file.write(soup.prettify())
            file.close()

        except NoSuchElementException:
            print('Some error occurred while trying to scroll down')
            self.error = True

    def target_button(self, index):
        target_button = self.driver.find_element_by_xpath(
            '//article[' + index + ']/div/div[1]/div[4]/div[2]/div[2]/form/button')
        self.driver.execute_script("arguments[0].scrollIntoView();", target_button)
        # target_button.click()

    def file_manager(self, ):
        bookings_folder_path = os.path.join(self.path, 'bookings')
        if not os.path.exists(bookings_folder_path):
            os.mkdir(bookings_folder_path)
        if self.error is False:
            self.write_bookings_to_excel_file(bookings_folder_path)
            print('Writing to excel ...')
        # if self.error is False:
        #     self.read_bookings_from_excel_file(self.path + '/bookings/bookings.xlsx')

    def write_bookings_to_excel_file(self, booking_path):
        # FIXME: openpyxl -> https://openpyxl.readthedocs.io/en/stable/index.html
        filepath = os.path.join(booking_path, 'bookings.xlsx')
        workbook = load_workbook(filepath)
        # todo: grab the active worksheet: worksheet = workbook.active
        # This is set to 0 by default. Unless you modify its value, you will always get the first worksheet by using:
        # worksheet = workbook.active
        # -> or you can create new worksheets using the Workbook.create_sheet() method:
        worksheet_1 = workbook.create_sheet("Snapshoot", 0)  # insert at first position
        worksheet_2 = workbook.create_sheet("Bookings", -1)  # insert at the penultimate position
        worksheet_3 = workbook.create_sheet("Stadistics")  # insert at the end (default)
        # Once you gave a worksheet a name, you can get it as a key of the workbook:
        # >>> ws3 = wb["New Title"]

        sheet = workbook.active
        sheet.column_dimensions['B'].number_format = '#,##0.00'
        header = ('Code', 'Price', 'Hotel', 'Zone', 'Retail', 'Profit')
        cell_reference = worksheet_1.cell(row=1, column=1)
        cell_reference.value = header[0]
        cell_reference = worksheet_1.cell(row=1, column=2)
        cell_reference.value = header[1]
        cell_reference = worksheet_1.cell(row=1, column=3)
        cell_reference.value = header[2]
        cell_reference = worksheet_1.cell(row=1, column=4)
        cell_reference.value = header[3]
        cell_reference = worksheet_1.cell(row=1, column=5)
        cell_reference.value = header[4]
        cell_reference = worksheet_1.cell(row=1, column=6)
        cell_reference.value = header[5]
        i = 2
        for row in self.data:
            # fixme: sheet.append(row) only append all rows, use cell instead:
            cell_reference = worksheet_1.cell(row=i, column=2)
            cell_reference.value = row[1]
            cell_reference = worksheet_1.cell(row=i, column=3)
            cell_reference.value = row[0]
            cell_reference = worksheet_1.cell(row=i, column=4)
            cell_reference.value = row[2]
            i += 1
        workbook.save(filepath)  # save file

    """
    def read_bookings_from_excel_file(self, excel_path):
        workbook = xlrd.open_workbook(excel_path)
        worksheet = workbook.sheet_by_index(0)
        for row in range(2):
            col_1, col_2, col_3, col_4, col_5, col_6 = worksheet.row_values(row)
            print(col_1, '    ', col_2, '    ', )

    def write_bookings_to_excel_file(self, booking_path):
        print('\nwriting to excel...')
        workbook = Workbook(os.path.join(booking_path, 'bookings.xlsx'))
        worksheet = workbook.add_worksheet()
        worksheet.set_column(2, 3, 50)
        worksheet.set_column(1, 1, 9)
        worksheet.set_column(4, 4, 9)
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format({'bold': True, 'italic': True, 'font_color': 'blue'})
        cell_money = workbook.add_format({'bold': True, 'italic': True, 'font_color': 'blue', 'num_format': '#,##0.00'})
        money = workbook.add_format({'num_format': '#,##0.00'})
        row = 0
        worksheet.write(row, 0, 'Code', bold)  # 3 --> row number, column number, value
        worksheet.write(row, 1, 'Price', bold)
        worksheet.write(row, 2, 'Hotel', bold)
        worksheet.write(row, 3, 'Address', bold)
        worksheet.write(row, 4, 'Retail', bold)
        worksheet.write(row, 5, 'Profit', bold)

        row += 1

        worksheet.write(row, 0, 'BEST', cell_money)
        worksheet.write(row, 1, self.cheap[1], cell_format)
        worksheet.write(row, 2, self.cheap[0], cell_format)
        worksheet.write(row, 3, self.cheap[2], cell_format)
        worksheet.write_formula(1, 4, '=1.374*B2', cell_money)
        worksheet.write_formula(1, 5, '=E2-B2', cell_money)
        row += 1

        for i, option in enumerate(self.options):
            if i < 9:
                worksheet.write(row, 0, 'AA0' + str(i + 1))
            else:
                worksheet.write(row, 0, 'AA' + str(i + 1))
            worksheet.write(row, 1, option[1], money)
            worksheet.write(row, 2, option[0])
            worksheet.write(row, 3, option[2])
            worksheet.write_array_formula('E3:E31', '{=1.374*B3:B31}', money)
            worksheet.write_array_formula('F3:F31', '{=E3:E31-B3:B31}', money)
            row += 1
        workbook.close()
        # fixme WARNING:
        # in order for xlsxwriter to create the spreadsheet, the workbook must be closed
        # right at the end. If it closes after it won't create it, check it by closing it after the line:
        # self.send_attachment (spreadsheet)
        spreadsheet = '//home/jmartorell/Booking/bookings/bookings.xlsx'
        self.send_attachment(spreadsheet)

    def send_attachment(self, file):
        subject = "An email with attachment from Python"
        body = "This is an email with attachment sent from Python"
        sender_email = "jetro4100@gmail.com"
        receiver_email = "martorelljosep@gmail.com"
        # password = input("Type your password and press enter:")
        password = 'ZXspectrum5128$}_'

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = file  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
    """


if __name__ == '__main__':
    app = App()
