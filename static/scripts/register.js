// register.js

// Function to validate the form fields
function validateForm() {
    let username = document.getElementById('username').value;
    let otherNames = document.getElementById('other_names').value;
    let email = document.getElementById('email').value;
    let phone = document.getElementById('phone').value;
    let physicalAddress = document.getElementById('physical_address').value;
    let nextOfKin = document.getElementById('next_of_kin').value;
    let password = document.getElementById('password').value;

    // Regular expression for validating phone number (basic check for digits)
    const phoneRegex = /^[0-9]{10}$/;

    // Clear previous error messages
    clearErrors();

    // Check if all fields are filled out
    if (!username || !otherNames || !email || !phone || !physicalAddress || !nextOfKin || !password) {
        showError("All fields are required.");
        return false;
    }

    // Check if email is in the correct format
    if (!validateEmail(email)) {
        showError("Please enter a valid email address.");
        return false;
    }

    // Check if phone number matches the regex pattern
    if (!phoneRegex.test(phone)) {
        showError("Phone number should be 10 digits long.");
        return false;
    }

    // Check if password is strong enough (min length 6)
    if (password.length < 6) {
        showError("Password must be at least 6 characters long.");
        return false;
    }

    return true; // Form is valid
}

// Function to validate email format
function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return emailRegex.test(email);
}

// Function to show error messages
function showError(message) {
    let errorContainer = document.createElement('div');
    errorContainer.classList.add('error-message');
    errorContainer.innerText = message;
    document.querySelector('.register-form').prepend(errorContainer);
}

// Function to clear error messages
function clearErrors() {
    let errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach((msg) => msg.remove());
}

// Add event listener to validate form before submission
document.querySelector('form').addEventListener('submit', function(event) {
    if (!validateForm()) {
        event.preventDefault(); // Prevent form submission if invalid
    }
});
