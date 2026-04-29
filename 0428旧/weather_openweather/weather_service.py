import requests

API_KEY = "7e61ea741a419369742bac830ec6bc60"
CITY = "Fukuoka"

def get_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }

    res = requests.get(url, params=params)
    data = res.json()

    if data.get("cod") != 200:
        return "Error", 0, "fa-triangle-exclamation"

    weather_main = data["weather"][0]["main"]
    temp = data["main"]["temp"]

    mapping = {
        "Clear": "fa-sun",
        "Clouds": "fa-cloud",
        "Rain": "fa-cloud-rain",
        "Drizzle": "fa-cloud-rain",
        "Thunderstorm": "fa-bolt",
        "Snow": "fa-snowflake",
        "Mist": "fa-smog",
        "Fog": "fa-smog"
    }

    icon = mapping.get(weather_main, "fa-cloud")

    return weather_main, temp, icon