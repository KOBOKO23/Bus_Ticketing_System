// user_bookings.js

// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", () => {
    // Form validation
    const bookingForm = document.querySelector(".booking-form");

    if (bookingForm) {
        bookingForm.addEventListener("submit", (event) => {
            const nameInput = document.getElementById("name");
            const phoneInput = document.getElementById("phone");
            const emailInput = document.getElementById("email");
            const passengersInput = document.getElementById("passengers");

            // Simple validation
            if (
                !nameInput.value.trim() ||
                !phoneInput.value.trim() ||
                !emailInput.value.trim() ||
                !passengersInput.value
            ) {
                event.preventDefault();
                alert("Please fill out all fields before submitting.");
            } else if (!/^\d{10}$/.test(phoneInput.value)) {
                event.preventDefault();
                alert("Please enter a valid 10-digit phone number.");
            } else if (!validateEmail(emailInput.value)) {
                event.preventDefault();
                alert("Please enter a valid email address.");
            }
        });
    }

    // Seats dropdown auto-populate
    const seatsDropdown = document.getElementById("passengers");
    if (seatsDropdown) {
        const maxSeats = 10; // Example max seats, adjust based on backend data
        for (let i = 1; i <= maxSeats; i++) {
            const option = document.createElement("option");
            option.value = i;
            option.textContent = i;
            seatsDropdown.appendChild(option);
        }
    }

    // Email validation function
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Highlight booking form fields on focus
    const inputs = document.querySelectorAll(".booking-form input, .booking-form select");
    inputs.forEach((input) => {
        input.addEventListener("focus", () => {
            input.style.borderColor = "#4CAF50"; // Change to a highlight color
        });

        input.addEventListener("blur", () => {
            input.style.borderColor = ""; // Reset to default
        });
    });

    // Success message handling
    const flashMessage = document.querySelector(".flash-message");
    if (flashMessage) {
        setTimeout(() => {
            flashMessage.style.display = "none";
        }, 5000); // Hide flash message after 5 seconds
    }
});
