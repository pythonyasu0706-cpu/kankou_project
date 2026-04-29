// food.js
// const mainImage = document.querySelector('.gallery-image img');
// const thumbImages = document.querySelectorAll('.gallery-thumbnails img');

// for (let i = 0; i < thumbImages.length; i++) {
//     thumbImages[i].addEventListener('mouseover', (event) => {
//         console.log(event);
//         mainImage.src = event.target.src;
//         mainImage.animate({ opacity: [0, 1] }, 500);
//     });
// }

(() => {
    const mainImage = document.querySelector('.gallery-image img');
    const thumbImages = document.querySelectorAll('.gallery-thumbnails img');

    if (!mainImage || thumbImages.length === 0) return;

    thumbImages.forEach(img => {
        img.addEventListener('mouseover', (e) => {
            mainImage.src = e.target.src;
            mainImage.animate({ opacity: [0, 1] }, 500);
        });
    });
})();