document.addEventListener('DOMContentLoaded', function() {
    // 1. Interactive Logout Button
    const logoutButton = document.querySelector('a[href="{{ url_for('logout') }}"]');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            const confirmation = confirm('Are you sure you want to log out?');
            if (!confirmation) {
                event.preventDefault(); // Prevent the logout if canceled
            }
        });
    }

    // 2. Scroll to Content Button
    const scrollButton = document.getElementById('scrollToContentBtn');
    if (scrollButton) {
        const contentSection = document.getElementById('content');
        scrollButton.addEventListener('click', function() {
            contentSection.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // 3. Dynamic Header (Hide/Show on Scroll)
    let lastScrollTop = 0;
    const header = document.getElementById('header');
    if (header) {
        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
            if (currentScroll > lastScrollTop) {
                header.style.top = "-60px";  // Adjust based on the header height
            } else {
                header.style.top = "0";
            }
            lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;  // Prevent negative scrolling
        });
    }

    // 4. Mobile Navigation Toggle
    const menuToggle = document.getElementById('menuToggle');
    const mobileNav = document.getElementById('mobileNav');
    if (menuToggle && mobileNav) {
        menuToggle.addEventListener('click', function() {
            if (mobileNav.style.display === 'none' || mobileNav.style.display === '') {
                mobileNav.style.display = 'block';
            } else {
                mobileNav.style.display = 'none';
            }
        });
    }

    // 5. Dynamic Footer Year
    const footerYear = document.querySelector('footer p');
    if (footerYear) {
        const currentYear = new Date().getFullYear();
        footerYear.innerHTML = `&copy; ${currentYear} Vuka Africa. All rights reserved.`;
    }
});
