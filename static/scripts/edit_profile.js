document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".edit-profile-form form");
    const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");
    const phoneInput = document.getElementById("phone");
    const passwordInput = document.getElementById("password");
    const saveButton = document.querySelector(".save-button");

    // Helper function for displaying validation messages
    const showValidationMessage = (input, message) => {
        let messageElement = input.nextElementSibling;
        if (!messageElement || !messageElement.classList.contains("validation-message")) {
            messageElement = document.createElement("span");
            messageElement.classList.add("validation-message");
            input.parentNode.appendChild(messageElement);
        }
        messageElement.textContent = message;
    };

    // Helper function for clearing validation messages
    const clearValidationMessage = (input) => {
        const messageElement = input.nextElementSibling;
        if (messageElement && messageElement.classList.contains("validation-message")) {
            messageElement.textContent = "";
        }
    };

    // Username validation
    usernameInput.addEventListener("input", () => {
        if (usernameInput.value.trim() === "") {
            showValidationMessage(usernameInput, "Username is required.");
        } else {
            clearValidationMessage(usernameInput);
        }
    });

    // Email validation
    emailInput.addEventListener("input", () => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value.trim())) {
            showValidationMessage(emailInput, "Enter a valid email address.");
        } else {
            clearValidationMessage(emailInput);
        }
    });

    // Phone number validation
    phoneInput.addEventListener("input", () => {
        const phoneRegex = /^[0-9]{10}$/;
        if (!phoneRegex.test(phoneInput.value.trim())) {
            showValidationMessage(phoneInput, "Enter a valid 10-digit phone number.");
        } else {
            clearValidationMessage(phoneInput);
        }
    });

    // Password strength indicator
    passwordInput.addEventListener("input", () => {
        if (passwordInput.value.trim() && passwordInput.value.length < 8) {
            showValidationMessage(passwordInput, "Password must be at least 8 characters long.");
        } else {
            clearValidationMessage(passwordInput);
        }
    });

    // Form submission validation
    form.addEventListener("submit", (event) => {
        let isValid = true;

        // Validate all fields
        if (usernameInput.value.trim() === "") {
            showValidationMessage(usernameInput, "Username is required.");
            isValid = false;
        }
        if (!emailInput.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
            showValidationMessage(emailInput, "Enter a valid email address.");
            isValid = false;
        }
        if (!phoneInput.value.match(/^[0-9]{10}$/)) {
            showValidationMessage(phoneInput, "Enter a valid 10-digit phone number.");
            isValid = false;
        }
        if (passwordInput.value && passwordInput.value.length < 8) {
            showValidationMessage(passwordInput, "Password must be at least 8 characters long.");
            isValid = false;
        }

        // Prevent form submission if validation fails
        if (!isValid) {
            event.preventDefault();
        }
    });

    // Save button hover effect
    saveButton.addEventListener("mouseenter", () => {
        saveButton.style.backgroundColor = "#4CAF50";
        saveButton.style.color = "#fff";
    });

    saveButton.addEventListener("mouseleave", () => {
        saveButton.style.backgroundColor = "";
        saveButton.style.color = "";
    });
});
