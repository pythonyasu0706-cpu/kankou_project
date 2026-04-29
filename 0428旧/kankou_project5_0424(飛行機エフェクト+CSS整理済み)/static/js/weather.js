const API_KEY = "7e61ea741a419369742bac830ec6bc60";
const CITY = "Fukuoka";

// ======================
// ① ヘッダー用（都市）
// ======================
async function getCityWeather() {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${CITY}&appid=${API_KEY}&units=metric&lang=ja`;

    const res = await fetch(url);
    const data = await res.json();

    const icon = data.weather[0].icon;
    const temp = Math.round(data.main.temp);

    const iconEl = document.getElementById("weather-icon");
    const tempEl = document.getElementById("weather-temp");

    if (iconEl) {
        iconEl.src = `https://openweathermap.org/img/wn/${icon}@2x.png`;
    }

    if (tempEl) {
        tempEl.textContent = `${temp}℃`;
    }
}

// ======================
// ② スポット用（座標）
// ======================
async function getPlaceWeather(place, elementId) {
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${place.lat}&lon=${place.lon}&appid=${API_KEY}&units=metric&lang=ja`;

    const res = await fetch(url);
    const data = await res.json();

    const temp = Math.round(data.main.temp);
    const weather = data.weather[0].description;
    const icon = data.weather[0].icon;
    const link = `https://weathernews.jp/onebox/${place.lat}/${place.lon}/`;

    const html = `
        <a href="${link}" target="_blank" class="weather-inline" title="${weather}">
            <img src="https://openweathermap.org/img/wn/${icon}.png">
            <span>${temp}℃</span>
            <span class="weather-btn">現地の天気</span>
        </a>
    `;

    const el = document.getElementById(elementId);
    if (el) el.innerHTML = html;
}

// ======================
// 起動
// ======================
document.addEventListener("DOMContentLoaded", () => {
    getCityWeather();

    getPlaceWeather(
        { lat: 33.5902, lon: 130.4017 },
        "tenjin-weather"
    );

    getPlaceWeather(
        { lat: 33.5898, lon: 130.4207 },
        "hakata-weather"
    );
});