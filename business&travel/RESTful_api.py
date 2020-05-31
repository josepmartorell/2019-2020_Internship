import sys
import requests
import dataset as d

base_url = 'http://api.openweathermap.org/data/2.5/weather'
api_key = '8b40250178cc702abaa5d8e4a89cfa79'
cities = [i[0] for i in d.tour_en]


def get_temperature(city):
    query = base_url + '?q=%s&units=metric&APPID=%s' % (city, api_key)
    try:
        response = requests.get(query)
        # print("[%s] %s" % (response.status_code, response.url))
        if response.status_code != 200:
            response = 'N/A'
            return response
        else:
            weather_data = response.json()  # todo
            return weather_data['main']['temp'], weather_data['main']['humidity']
    except requests.exceptions.RequestException as error:
        print(error)
        sys.exit(1)


def main():
    for city in cities:
        location = get_temperature(city)
        print("temperat ", city, ": ", location[0])
        print("humidity ", city, ": ", location[1])


if __name__ == '__main__':
    main()

# TODO: fix TypeError: string indices must be integers, not str if base_url is incorrect
