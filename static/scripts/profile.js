document.addEventListener('DOMContentLoaded', function() {

    // Image upload functionality
    const profileImageContainer = document.querySelector('.profile-image img');
    const profileImageInput = document.getElementById('profile-image-input');
    const profileImageDisplay = document.querySelector('.profile-image img');

    if (profileImageContainer && profileImageInput) {
        // Click on image triggers file input dialog
        profileImageContainer.addEventListener('click', function() {
            profileImageInput.click();
        });

        // Update image preview on file selection
        profileImageInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                if (!file.type.startsWith('image/')) {
                    alert('Please upload a valid image file.');
                    return;
                }
                const reader = new FileReader();
                reader.onload = function(e) {
                    profileImageDisplay.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
