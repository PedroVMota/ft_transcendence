document.addEventListener('DOMContentLoaded', function () {
    const menuLinks = document.querySelectorAll('nav a[data-url]');

    menuLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.getAttribute('data-url');

            fetch(url)
                .then(response => response.text())
                .then(html => {
                    console.log('Page loaded:', html);
                    document.getElementById('SinglePageApplicationRoot').innerHTML = html;
                })
                .catch(error => {
                    console.error('Error loading the page:', error);
                });
        });
    });
});