import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from geopy import Nominatim
from datetime import datetime

def geo(text):
    geolocator = Nominatim(user_agent="meteo_app")
    location = geolocator.geocode(text)
    return location.latitude, location.longitude


def meteo(latitude, longitude):

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability", "precipitation", "wind_speed_10m", "surface_pressure"],
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "pressure_msl", "wind_direction_10m", "wind_speed_10m"],
        "timezone": "auto",
        "forecast_days": 1,
        "timeformat": "unixtime",
        "wind_speed_unit": "ms",
        "forecast_hours": 4
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    data = {}

    current = response.Current()
    data['current'] = {
        'time': datetime.fromtimestamp(current.Time()).strftime('%d.%m.%Y %H:%M:%S'),
        'current_temp': round(current.Variables(0).Value(), 2),
        'current_humidity': current.Variables(1).Value(),
        'current_feel_temp': round(current.Variables(2).Value(), 2),
        'current_precipitation': current.Variables(3).Value() * 100,
        'current_pressure': round(current.Variables(4).Value(), 2),
    }

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()

    hourly_dict = {}

    for i in range(0,4):
        hourly_dict[i] = {
            'temp': hourly.Variables(0).Values(i),
            'humidity': hourly.Variables(1).Values(i),
            'feeltemp': round(hourly.Variables(2).Values(i), 2),
            'pressure': round(hourly.Variables(6).Values(i), 1),
            'precipitation': hourly.Variables(4).Values(i),
            'wind': round(hourly.Variables(5).Values(i), 1),
        }

    data['hourly'] = hourly_dict

    return data