import sys
import requests

base_url = 'http://api.openweathermap.org/data/2.5/weather'
api_key = '8b40250178cc702abaa5d8e4a89cfa79'


# cities = [i[0] for i in d.tour_en]


def get_humidity(city):
    query = base_url + '?q=%s&units=metric&APPID=%s' % (city, api_key)
    try:
        response = requests.get(query)
        # print("[%s] %s" % (response.status_code, response.url))
        if response.status_code != 200:
            response = 'N/A'
            return response
        else:
            weather_data = response.json()
            return weather_data['main']['humidity']
    except requests.exceptions.RequestException as error:
        print(error)
        sys.exit(1)


def get_temperature(city):
    query = base_url + '?q=%s&units=metric&APPID=%s' % (city, api_key)
    try:
        response = requests.get(query)
        # print("[%s] %s" % (response.status_code, response.url))
        if response.status_code != 200:
            response = 'N/A'
            return response
        else:
            weather_data = response.json()
            return weather_data['main']['temp']
    except requests.exceptions.RequestException as error:
        print(error)
        sys.exit(1)

