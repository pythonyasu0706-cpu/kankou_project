// food.js

(() => {
    const mainImage = document.querySelector('.gallery-image img');
    const thumbImages = document.querySelectorAll('.gallery-thumbnails img');
    const title = document.querySelector('#gallery-title');

    if (!mainImage || thumbImages.length === 0) return;

    // 初期表示をJSで統一
    mainImage.src = thumbImages[0].src;
    if (title) title.textContent = thumbImages[0].dataset.title;

    thumbImages.forEach(img => {
        img.addEventListener('mouseover', (e) => {
            mainImage.src = e.target.src;

            // ▼ここ追加
            if (title) {
                title.textContent = e.target.dataset.title;
            }

            mainImage.animate({ opacity: [0, 1] }, 500);
        });
    });
})();