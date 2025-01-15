document.addEventListener("DOMContentLoaded", () => {
    // Elements
    const form = document.querySelector(".booking-form");
    const nameInput = document.getElementById("name");
    const phoneInput = document.getElementById("phone");
    const emailInput = document.getElementById("email");
    const dateInput = document.getElementById("date");
    const passengersSelect = document.getElementById("passengers");

    // Validation Functions
    function validatePhone(phone) {
        const phoneRegex = /^[0-9]{10}$/;
        return phoneRegex.test(phone);
    }

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Form Submit Handler
    form.addEventListener("submit", (event) => {
        let hasError = false;

        // Validate Name
        if (!nameInput.value.trim()) {
            alert("Name is required!");
            hasError = true;
        }

        // Validate Phone
        if (!validatePhone(phoneInput.value)) {
            alert("Please enter a valid 10-digit phone number.");
            hasError = true;
        }

        // Validate Email
        if (!validateEmail(emailInput.value)) {
            alert("Please enter a valid email address.");
            hasError = true;
        }

        // Validate Date
        if (!dateInput.value) {
            alert("Please select a date.");
            hasError = true;
        }

        // Validate Passengers
        if (!passengersSelect.value) {
            alert("Please select the number of passengers.");
            hasError = true;
        }

        // Prevent Form Submission if There Are Errors
        if (hasError) {
            event.preventDefault();
        }
    });
});
