// booking_confirmation.js

document.addEventListener("DOMContentLoaded", function () {
    // Action button event handlers
    const bookAnotherTicketBtn = document.querySelector(".btn-primary");
    if (bookAnotherTicketBtn) {
        bookAnotherTicketBtn.addEventListener("click", function () {
            console.log("Navigating to book another ticket...");
            // Add smooth scroll or transition to booking page if needed
            window.location.href = "/book-another-ticket"; // Assuming booking page URL
        });
    }

    // Optional: Add a feature to download the ticket if implemented
    const downloadTicketBtn = document.querySelector(".btn-secondary");
    if (downloadTicketBtn) {
        downloadTicketBtn.addEventListener("click", function (event) {
            event.preventDefault();
            // Enhance message for unimplemented feature
            alert("The ticket download feature is not implemented yet. Please check back later!");
            console.log("Download ticket feature clicked, but not yet implemented.");
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

    // Validate if all necessary details are present
    const missingDetails = Object.entries(bookingDetails)
        .filter(([key, value]) => !value)
        .map(([key]) => key);

    if (missingDetails.length > 0) {
        const missingMessage = `Some booking details are missing: ${missingDetails.join(', ')}. Please contact support.`;
        alert(missingMessage);
        console.error("Missing booking details:", missingMessage);
    } else {
        console.log("Booking Details:", bookingDetails);
    }

    // Optional: Adding confirmation for successful booking
    if (bookingDetails.bookingId) {
        const successMessage = `Your booking (ID: ${bookingDetails.bookingId}) has been confirmed!`;
        const successElement = document.createElement('div');
        successElement.className = "booking-success-message";
        successElement.innerHTML = `<p>${successMessage}</p>`;
        document.body.insertBefore(successElement, document.body.firstChild);
    }
});
