// static/js/form.js
document.addEventListener("DOMContentLoaded", function () {
    const agreeCheck = document.getElementById("agree-check");
    const submitBtn = document.getElementById("submit-btn");

    console.log(agreeCheck);
    console.log(submitBtn);

    if (agreeCheck && submitBtn) {
        agreeCheck.addEventListener("change", function () {
            submitBtn.disabled = !agreeCheck.checked;
        });
    }
});