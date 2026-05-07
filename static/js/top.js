// static/js/top.js トップページの飛行機

// const slides = document.querySelectorAll(".slider img");
// let slides = document.querySelectorAll(".slider img");
// let i = 0;

// setInterval(() => {
//     slides[i].classList.remove("active");
//     i = (i + 1) % slides.length;
//     slides[i].classList.add("active");
// }, 4000);

// static/js/top.js トップページの飛行機


const slides = document.querySelectorAll(".slider img");
// let slides = document.querySelectorAll(".slider img");
let i = 0;


setInterval(() => {
    slides[i].classList.remove("active");
    i = (i + 1) % slides.length;
    slides[i].classList.add("active");
}, 4000);


// static/js/top.js information
document.addEventListener("DOMContentLoaded", function () {
    console.log("JS読み込みOK");


    const items = document.querySelectorAll(".info-item");
    const today = new Date();


    items.forEach(item => {
        const dateEl = item.querySelector(".info-date");


        // data-date無いならスキップ
        if (!dateEl || !dateEl.dataset.date) {
            console.log("data-dateなし");
            return;
        }


        const itemDate = new Date(dateEl.dataset.date);


        console.log("比較:", today, itemDate);


        const diffTime = today - itemDate;
        const diffDays = diffTime / (1000 * 60 * 60 * 24);


        console.log("日数差:", diffDays);


        if (diffDays <= 3 && diffDays >= 0) {
            const badge = document.createElement("span");
            badge.className = "new-badge";
            badge.textContent = "NEW";


            item.querySelector(".info-text").prepend(badge);
        }
    });
});
