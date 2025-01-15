// forgot_password.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const emailInput = document.getElementById("email");
    const submitButton = form.querySelector("button[type='submit']");
    
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        
        // Validate the email input
        const email = emailInput.value.trim();
        if (!validateEmail(email)) {
            alert("Please enter a valid email address.");
            return;
        }
        
        // Disable submit button to prevent multiple submissions
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";

        // Perform AJAX request to handle password recovery
        fetch("/password-recovery", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Password reset link has been sent to your email.");
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch((error) => {
            console.error("Error during password recovery:", error);
            alert("Something went wrong. Please try again later.");
        })
        .finally(() => {
            // Re-enable the submit button
            submitButton.disabled = false;
            submitButton.textContent = "Submit";
        });
    });

    // Email validation function
    function validateEmail(email) {
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return emailPattern.test(email);
    }
});
