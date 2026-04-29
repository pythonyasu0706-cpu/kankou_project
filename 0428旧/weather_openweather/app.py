import requests
import time
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = "7e61ea741a419369742bac830ec6bc60"
CITY = "Fukuoka"

last_fetch = 0
cached_icon = None


def get_weather():
    global last_fetch, cached_icon

    # 10分キャッシュ
    if time.time() - last_fetch < 600 and cached_icon:
        return cached_icon

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}"
        f"&appid={API_KEY}"
        f"&units=metric"
        f"&lang=ja"
    )

    res = requests.get(url)
    data = res.json()

    # OpenWeatherの icon code をそのまま取得
    icon = data["weather"][0]["icon"]
    temp = data["main"]["temp"]

    weather_data = {
        "icon": icon,
        "temp": round(temp)
    }

    cached_icon = weather_data
    last_fetch = time.time()

    return weather_data


@app.route("/")
def index():
    weather = get_weather()
    return render_template(
        "index.html",
        weather=weather
    )


if __name__ == "__main__":
    app.run(debug=True)