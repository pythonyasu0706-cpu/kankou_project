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
});

// ===================
// タブ処理のJS
// ===================

document.addEventListener("DOMContentLoaded", function () {
    // タブ切り替え
    const root = document.getElementById("tab-root");
    const activeTab = root.dataset.activeTab || "new";

    // タブ初期化
    document.querySelectorAll(".tab-content").forEach(el => {
        el.classList.remove("active");
    });
    document.getElementById(activeTab).classList.add("active");

    // ボタンも
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.classList.remove("active");
    });
    document.querySelector(`[data-tab="${activeTab}"]`).classList.add("active");
});

// ===================
// タブ切り替えのJS
// ===================

document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const tab = btn.dataset.tab;

        // ボタン切り替え
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        // コンテンツ切り替え
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
        document.getElementById(tab).classList.add("active");
    });
});