// profile.js

document.addEventListener('DOMContentLoaded', function() {

    // Image upload functionality
    const profileImageInput = document.getElementById('profile-image-input');
    const profileImageDisplay = document.querySelector('.profile-image img');

    if (profileImageInput) {
        profileImageInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    profileImageDisplay.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Edit Profile button functionality (if you want to display confirmation or message)
    const editProfileBtn = document.querySelector('.edit-profile .btn');
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', function(event) {
            // Optional: display a confirmation modal before allowing edits
            const confirmEdit = confirm("Are you sure you want to edit your profile?");
            if (!confirmEdit) {
                event.preventDefault();
            }
        });
    }

    // Add any other JavaScript enhancements as needed
});
