# import package
from bs4 import BeautifulSoup


# source
def read_file():
    file = open('solole.html')
    data = file.read()
    file.close()
    return data


# make soup
html_file = read_file()
soup = BeautifulSoup(html_file, 'lxml')

# tag.contents returns us direct children of the said tag for example FOOTER in [2] position
'''body = soup.body
children = [child for child in body.contents if child != '\n']
for child in children:
    print(child)'''

# hotel_list = soup.find_all('div', {'class': 'my-4'})  # name, price and address approached scope
# fixme price: price_list = soup.find_all('div', {'class': 'text-main-light prices'})  # price display ok
# fixme name: hotel_list = soup.find_all('div', {'class': 'row result-option'}) # name display ok
# fixme address: address_list = soup.find_all('div', {'class': 'address'})  # address display ok
# hotel_list = soup.find_all('', {'': ''})
# hotel_list = soup.find_all('', {'': ''})

# print(hotel_list)

price_list = soup.find_all('div', {'class': 'text-main-light prices'})
# fixme: price mechanism:
euro_symbol = '€'
for i, price in enumerate(price_list):
    hotel_price = price.find('span', {'_ngcontent-c18': ""}).getText().replace('€', '')
    hotel_price = ' '.join(hotel_price.split())
    print(" %d - %s %s" % (i + 1, hotel_price, euro_symbol))

print('\n')

hotel_list = soup.find_all('div', {'class': 'row result-option'})
# fixme: name mechanism:
for i, hotel in enumerate(hotel_list):
    hotel_name = hotel.find('span', {'_ngcontent-c18': ""}).getText()
    hotel_name = ' '.join(hotel_name.split())
    print("%d - %s" % (i + 1, hotel_name))

print('\n')

address_list = soup.find_all('div', {'class': 'address'})
# fixme: address mechanism:
for i, address in enumerate(address_list):
    hotel_address = address.find('span', {'_ngcontent-c18': ""}).getText()
    hotel_address = ' '.join(hotel_address.split())
    print("%d - %s" % (i + 1, hotel_address))