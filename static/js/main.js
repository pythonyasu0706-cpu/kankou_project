// // static/js/main.js 共通JS

(() => {
    // ハンバーガー
    const hamburger = document.getElementById("hamburger");
    const nav = document.getElementById("nav");

    if (hamburger && nav) {
        hamburger.addEventListener("click", () => {
            hamburger.classList.toggle("active");
            nav.classList.toggle("active");
        });
    }

    // ギャラリー
    const mainImage = document.querySelector('.gallery-image img');
    const thumbImages = document.querySelectorAll('.gallery-thumbnails img');

    if (mainImage && thumbImages.length > 0) {
        thumbImages.forEach(img => {
            img.addEventListener('mouseover', (event) => {
                mainImage.src = event.target.src;
                mainImage.animate({ opacity: [0, 1] }, 500);
            });
        });
    }
})();



/* ===================
    Weather Icon用のJS 開始
=================== */

const CITY = "Fukuoka";
const API_KEY = window.API_KEY;

if (!API_KEY) {
    console.error("API_KEYが設定されていません");
}

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
    // ヘッダー天気    
    getCityWeather(); 

    // スポット天気
    if (typeof spots !== "undefined") {
        spots.forEach(spot => {
            getPlaceWeather(
                { lat: spot.lat, lon: spot.lon },
                spot.weather_id
            );
        });
    }
});

/* ===================
    Weather Icon用のJS 終了
=================== */

// ふわっとでるアニメーション
document.addEventListener("DOMContentLoaded", function () {

    // ① main内の全要素に fadeanimation をつける
    // ▼ アクセスページのメイン画像内の文字ズレ回避のためにheroを追加
    document.querySelectorAll("main *:not(.hero):not(.hero *)")
        .forEach(el => {
            el.classList.add("fadeanimation");
        });

    // ② スクロール検知
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: "0px 0px -100px 0px",
        threshold: 0
    });

    // ③ 監視開始
    document.querySelectorAll(".fadeanimation")
        .forEach(el => observer.observe(el));

});