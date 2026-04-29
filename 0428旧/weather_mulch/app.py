import requests
import time
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = "7e61ea741a419369742bac830ec6bc60"

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

        results.append({
            "name": place["name"],
            "temp": round(data["main"]["temp"]),
            "weather": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "url": f"https://weathernews.jp/onebox/{place['lat']}/{place['lon']}/"
        })

    return results


@app.route("/")
def index():
    results = get_weather()
    return render_template(
        "index.html",
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)