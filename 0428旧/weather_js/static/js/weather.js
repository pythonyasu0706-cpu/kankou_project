const API_KEY = "7e61ea741a419369742bac830ec6bc60";

async function getWeather(place, elementId) {
  const url = "https://api.openweathermap.org/data/2.5/weather";

  const params = `?lat=${place.lat}&lon=${place.lon}&appid=${API_KEY}&units=metric&lang=ja`;

  const res = await fetch(url + params);
  const data = await res.json();

  const temp = Math.round(data.main.temp);
  const weather = data.weather[0].description;
  const icon = data.weather[0].icon;
  const link = `https://weathernews.jp/onebox/${place.lat}/${place.lon}/`;

  const html = `
    <div class="weather-box">
      <a href="${link}" target="_blank">
        <p>${place.name}</p>
        <img src="https://openweathermap.org/img/wn/${icon}@2x.png">
        <p>${temp}℃</p>
        <p>${weather}</p>
      </a>
    </div>
  `;

  document.getElementById(elementId).innerHTML = html;
}

// 個別に呼ぶ
getWeather(
  { name: "天神", lat: 33.5902, lon: 130.4017 },
  "tenjin-weather"
);

getWeather(
  { name: "博多駅", lat: 33.5898, lon: 130.4207 },
  "hakata-weather"
);