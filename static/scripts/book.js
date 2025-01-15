// book.js

document.addEventListener("DOMContentLoaded", function () {
    // Highlight the selected option in the dropdown
    const passengerDropdown = document.getElementById("passengers");
    if (passengerDropdown) {
        passengerDropdown.addEventListener("change", function () {
            const selectedValue = this.value;
            console.log(`Number of Passengers Selected: ${selectedValue}`);
        });
    }

    // Form validation and feedback
    const bookingForm = document.querySelector(".booking-form");
    if (bookingForm) {
        bookingForm.addEventListener("submit", function (event) {
            const name = document.getElementById("name").value.trim();
            const phone = document.getElementById("phone").value.trim();
            const email = document.getElementById("email").value.trim();

            if (!name || !phone || !email) {
                event.preventDefault();
                alert("Please fill out all required fields.");
                return;
            }

            if (!/^\d{10}$/.test(phone)) {
                event.preventDefault();
                alert("Please enter a valid 10-digit phone number.");
                return;
            }

            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                event.preventDefault();
                alert("Please enter a valid email address.");
                return;
            }

            alert("Form submitted successfully!");
        });
    }

    // Pre-fill user data in the form (if available)
    const userName = "{{ user_data.name|escapejs }}";
    const userPhone = "{{ user_data.phone|escapejs }}";
    const userEmail = "{{ user_data.email|escapejs }}";

    if (userName) {
        document.getElementById("name").value = userName;
    }
    if (userPhone) {
        document.getElementById("phone").value = userPhone;
    }
    if (userEmail) {
        document.getElementById("email").value = userEmail;
    }
});
