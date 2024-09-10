# Weather Application for CLI

## Description
Using the API from Open Weather https://openweathermap.org/, the application is able to make calls for the current weather or a 5 day forecast for an inputted city. The app receives input from the user by the command line interface and uses the user inputs to receive the weather data. The weather data is displayed in a readable format on the command line.

![Weather App help command photo](/Photos/weather_app_help.png)

## Requirements
- Python 3.9 environment
- OpenWeather API key (create secret.ini file with following line "api_key={Your API key}"

## What it Does
Displays the current weather for the city inputted, defaults in metric units, option for imperial units.
"python WeatherAppCLI.py city -c" or "python WeatherAppCLI.py -c -i"

![Weather App current weather](/Photos/weather_app_current.png)

Displays the forecast weather for the next 5 days in 3 hour increments, defaults in metric units, option for imperial units.

![Weather App forecast weather 1](/Photos/weather_app_forecast_1.png)
![Weather App forecast weather 2](/Photos/weather_app_forecast_2.png)
![Weather App forecast weather 3](/Photos/weather_app_forecast_3.png)
![Weather App forecast weather 4](/Photos/weather_app_forecast_4.png)

## Resources
OpenWeather
https://openweathermap.org/current#name
https://openweathermap.org/forecast5

https://realpython.com/build-a-python-weather-app-cli/
Helpful tutorial

### Created by
James Bird-Sycamore  10/09/2024
