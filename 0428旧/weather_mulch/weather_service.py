import requests

API_KEY = "7e61ea741a419369742bac830ec6bc60"
CITY = "Fukuoka"


def get_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"

    places = [
        {
            "name": "天神",
            "lat": 33.5902,
            "lon": 130.4017
        },
        {
            "name": "博多駅",
            "lat": 33.5898,
            "lon": 130.4207
        }
    ]

    results = []

    for place in places:
        params = {
            "lat": place["lat"],
            "lon": place["lon"],
            "appid": API_KEY,
            "units": "metric",
            "lang": "ja"
        }

        res = requests.get(url, params=params)
        data = res.json()

        lat = place["lat"]
        lon = place["lon"]

        results.append({
            "name": place["name"],
            "temp": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],

            # ★ここがポイント
            "url": f"https://weathernews.jp/onebox/{lat}/{lon}/"
        })

    return results