// static/js/main.js
// ハンバーガーメニューの動作
const hamburger = document.getElementById("hamburger");
const nav = document.getElementById("nav");

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    nav.classList.toggle("active");
});


// グルメとスポットページのギャラリーのためのJS
const mainImage = document.querySelector('.gallery-image img');
const thumbImages = document.querySelectorAll('.gallery-thumbnails img');

for (let i = 0; i < thumbImages.length; i++) {
    thumbImages[i].addEventListener('mouseover', (event) => {
        console.log(event);
        mainImage.src = event.target.src;
        mainImage.animate({ opacity: [0, 1] }, 500);
    });
}