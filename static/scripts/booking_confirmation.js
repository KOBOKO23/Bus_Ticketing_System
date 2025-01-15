// booking_confirmation.js

document.addEventListener("DOMContentLoaded", function () {
    // Action button event handlers
    const bookAnotherTicketBtn = document.querySelector(".btn-primary");
    if (bookAnotherTicketBtn) {
        bookAnotherTicketBtn.addEventListener("click", function () {
            console.log("Navigating to book another ticket...");
        });
    }

    // Optional: Add a feature to download the ticket if implemented
    const downloadTicketBtn = document.querySelector(".btn-secondary");
    if (downloadTicketBtn) {
        downloadTicketBtn.addEventListener("click", function (event) {
            event.preventDefault();
            alert("This feature is not implemented yet!");
            // Implement the download functionality if required
        });
    }

    // Display a message if there are any missing booking details
    const bookingDetails = {
        bookingId: "{{ booking.booking_id|escapejs }}",
        name: "{{ booking.name|escapejs }}",
        passengers: "{{ booking.passengers|escapejs }}",
        phone: "{{ booking.phone|escapejs }}",
        email: "{{ booking.email|escapejs }}",
        origin: "{{ booking.origin|escapejs }}",
        destination: "{{ booking.destination|escapejs }}",
        departure: "{{ booking.departure|escapejs }}",
        arrival: "{{ booking.arrival|escapejs }}",
        cost: "{{ booking.cost|escapejs }}"
    };

    if (!bookingDetails.bookingId) {
        alert("Some booking details are missing. Please contact support.");
    }

    console.log("Booking Details:", bookingDetails);
});
