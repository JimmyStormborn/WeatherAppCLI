'''
WeatherAppCLI.py

Project to create a weather application which retrieves the current
weather in London from OpenWeather and can show it in the CLI.

@author James Bird-Sycamore
@created 04/09/2024
@updated 04/09/2024
'''

import argparse
import json
import sys
from configparser import ConfigParser
from urllib import error, parse, request

import style

BASE_WEATHER_API_API = 'http://api.openweathermap.org/data/2.5/weather'

# Weather Condition Codes
# https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)

# Wind Direction Codes
SOUTH = range(-15, 15)
SOUTHWEST = range(15, 75)
WEST = range(75, 105)
NORTHWEST = range(105, 165)
NORTH = range(165, 195)
NORTHEAST = range(195, 255)
EAST = range(255, 285)
SOUTHEAST = range(285, 345)

def _get_api_key():
    '''Fetches the OpenWeather API key from the secrets.ini file.'''
    config = ConfigParser()
    config.read('secrets.ini')
    return config['openweather']['api_key']

def read_user_cli_args():
    '''
    Handles the CLI user interactions.

    Returns:
        argparse.Namespace   
    '''
    parser = argparse.ArgumentParser(description='Weather app retrieves weather information for a city',
                                     epilog='Thank you for visiting!')
    parser.add_argument('city', nargs='+', type=str, help='enter a city name')
    parser.add_argument('-i', '--imperial', action='store_true', help='display temperature in Farenheit')

    return parser.parse_args()

def build_weather_query(city_input, imperial=False):
    '''
    Builds the URL for an API request to OpenWeather's API.

    Args:
        from argparse user input

    Returns:
        str: Formatted URL
    '''
    api_key = _get_api_key()
    cityName = ' '.join(city_input)
    url_encoded_cityName = parse.quote_plus(cityName)
    units = 'imperial' if imperial else 'metric'
    url = (
        f'{BASE_WEATHER_API_API}?q={url_encoded_cityName}'
        f'&units={units}&appid={api_key}'
        )
    return url

def get_weather_data(query_url):
    '''
    Makes an API request to a URL and returns the data as a Python object.

    Args:
        query_url (str): URL formatted for OpenWeather's city name endpoint

    Returns:
        dict: Weather information for a specific city
    '''
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error == 401: # 401 - Unauthorized
            sys.exit("Access denied. Check API key")
        elif http_error == 404: # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong. {http_error.code}")

    data = response.read()

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("couldn't read the server response.")

def display_weather_info(weather_data, imperial=False):
    '''
    Displays the weather information from the data in a readable format.

    Args:
        weather_data (dict): API response
        imperial (bool): Fahrenhiet units when true

    More information at https://openweathermap.org/current#name
    '''
    city = weather_data['name']
    weather_id = weather_data["weather"][0]["id"]
    weatherDescription = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    windSpeed = weather_data['wind']['speed']
    wind_deg = weather_data['wind']['deg']

    # print city
    style.change_colour(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end=" ")
    style.change_colour(style.RESET)

    weatherSymbol, colour = _select_weather_display_params(weather_id)

    # print weather description
    style.change_colour(colour)
    print(f"\t{weatherSymbol}", end=" ")
    print(f"{weatherDescription.capitalize():^{style.PADDING}}", end=" ")
    style.change_colour(style.RESET)

    # print wind
    windSymbol = _select_wind_display_params(wind_deg)
    print(f"\n {windSymbol}", end=" ")
    print(f"\t{windSpeed}{'mph' if imperial else 'm/s'}", end=" ")

    # print temperature
    print(f"\n ({temperature} {'F' if imperial else 'C'})")

def _select_weather_display_params(weather_id):
    if weather_id in THUNDERSTORM:
        displayParams = ("⛈️", style.RED)
    elif weather_id in DRIZZLE:
        displayParams = ("🌦️", style.CYAN)
    elif weather_id in RAIN:
        displayParams = ("🌧️", style.BLUE)
    elif weather_id in SNOW:
        displayParams = ("🌨️", style.WHITE)
    elif weather_id in ATMOSPHERE:
        displayParams = ("🌤️", style.BLUE)
    elif weather_id in CLEAR:
        displayParams = ("☀️", style.YELLOW)
    elif weather_id in CLOUDY:
        displayParams = ("☁️", style.WHITE)
    else:
        displayParams = ("", style.RESET)
    return displayParams

def _select_wind_display_params(wind_deg):
    if wind_deg in NORTH:
        displayWind = "⬆️ Northerly"
    elif wind_deg in NORTHEAST:
        displayWind = "↗️ North Easterly"
    elif wind_deg in EAST:
        displayWind = "➡ Easterly"
    elif wind_deg in SOUTHEAST:
        displayWind = "↘️ South Easterly"
    elif wind_deg in SOUTH:
        displayWind = "⬇️ Southerly"
    elif wind_deg in SOUTHWEST:
        displayWind = "↙️ South Westerly"
    elif wind_deg in WEST:
        displayWind = "⬅️ Easterly"
    else:
        displayWind = "?"
    return displayWind

# Main
if __name__ == '__main__':
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)
    display_weather_info(weather_data, user_args.imperial)