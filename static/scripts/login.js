// login.js

document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('form');
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const errorMessagesDiv = document.querySelector('.error-messages');
    
    // Handle form submission
    loginForm.addEventListener('submit', function (event) {
        let isValid = true;
        errorMessagesDiv.innerHTML = ''; // Clear previous error messages

        // Basic validation: Check if email and password are filled
        if (!emailInput.value.trim()) {
            isValid = false;
            displayErrorMessage('Please enter your email address.');
        }

        if (!passwordInput.value.trim()) {
            isValid = false;
            displayErrorMessage('Please enter your password.');
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if there are errors
        }
    });

    // Function to display error messages
    function displayErrorMessage(message) {
        const messageElement = document.createElement('p');
        messageElement.textContent = message;
        errorMessagesDiv.appendChild(messageElement);

        // Add fade-in animation to the error message
        messageElement.classList.add('fade-in');
    }

    // Add dynamic input focus effect
    emailInput.addEventListener('focus', function () {
        emailInput.style.borderColor = '#007bff';
    });

    emailInput.addEventListener('blur', function () {
        emailInput.style.borderColor = '#ddd';
    });

    passwordInput.addEventListener('focus', function () {
        passwordInput.style.borderColor = '#007bff';
    });

    passwordInput.addEventListener('blur', function () {
        passwordInput.style.borderColor = '#ddd';
    });
});
