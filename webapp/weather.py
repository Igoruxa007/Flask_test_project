import requests

from flask import current_app


def weather_by_city():
    weather_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": current_app.config['WEATHER_API_KEY'],
        "q": current_app.config['WEATHER_DEFAULT_CITY'],
        "aqi": "no",
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather = result.json()
        if 'current' in weather:
            if 'temp_c' in weather['current']:
                try:
                    return weather['current']
                except(IndexError, TypeError):
                    return False
        return False
    except(requests.RequestException, ValueError):
        return False


if __name__ == "__main__":
    weather= weather_by_city()
    print(weather)