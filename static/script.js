document.addEventListener('DOMContentLoaded', function () {

    // Functionality to show password
    const show_password = document.querySelector("#show_password");
    const show_confirm_password = document.querySelector("#show_confirm_password");
    const user_password = document.querySelector("#user_password");
    const confirm_password = document.querySelector("#confirm_password");
    const passwordError1 = document.querySelector("#passwordError1");
    const passwordError2 = document.querySelector("#passwordError2");

    show_password.addEventListener("click", () => {
        if (user_password.type === "password") {
            user_password.type = "text";
            show_password.classList = "bi bi-eye";
        } else {
            user_password.type = "password";
            show_password.classList = "bi bi-eye-slash";
        }
    });

    show_confirm_password.addEventListener("click", () => {
        if (confirm_password.type === "password") {
            confirm_password.type = "text";
            show_confirm_password.classList = "bi bi-eye";
        } else {
            confirm_password.type = "password";
            show_confirm_password.classList = "bi bi-eye-slash";
        }
    });

    function validatePassword() {
        if (user_password.value != confirm_password.value) {
            // passwordError1.innerHTML = "Passwords do not match";
            passwordError2.innerHTML = "Passwords do not match";
            show_confirm_password.style.top = "35%";
        } else {
            // passwordError1.innerHTML = "";
            passwordError2.innerHTML = "";
            show_confirm_password.style.top = "47%";
        }
    }

    // user_password.addEventListener("keyup", validatePassword);
    confirm_password.addEventListener("keyup", validatePassword);

});