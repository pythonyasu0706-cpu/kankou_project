// static/js/form.js
// document.addEventListener("DOMContentLoaded", function () {
//     const agreeCheck = document.getElementById("agree-check");
//     const submitBtn = document.getElementById("submit-btn");

//     console.log(agreeCheck);
//     console.log(submitBtn);

//     if (agreeCheck && submitBtn) {
//         agreeCheck.addEventListener("change", function () {
//             submitBtn.disabled = !agreeCheck.checked;
//         });
//     }
// });

document.addEventListener("DOMContentLoaded", function () {
    const agreeCheck = document.getElementById("agree-check");
    const submitBtn = document.getElementById("submit-btn");

    console.log(agreeCheck);
    console.log(submitBtn);

    if (agreeCheck && submitBtn) {

        function toggleSubmitButton() {
            submitBtn.disabled = !agreeCheck.checked;
        }

        // 初期表示時に実行
        toggleSubmitButton();

        // チェック変更時
        agreeCheck.addEventListener("change", toggleSubmitButton);
    }

    // エラー位置スクロール
    const firstError = document.querySelector(".error-msg");

    if (firstError) {
        const field = firstError.closest(".form-group");

        field.scrollIntoView({
            behavior: "smooth",
            // block: "center"
            block: "start"
        });

        field.focus?.();
    }
});
