// index.js

document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.querySelector(".search-form form");
    const originSelect = document.getElementById("origin");
    const destinationSelect = document.getElementById("destination");

    // Validate the form before submission
    searchForm.addEventListener("submit", function (event) {
        // Check if origin and destination are selected
        if (!originSelect.value || !destinationSelect.value) {
            event.preventDefault(); // Prevent form submission
            alert("Please select both origin and destination.");
        }
    });

    // Optional: Add more interactivity here, like enabling/disabling form elements based on selection
});
