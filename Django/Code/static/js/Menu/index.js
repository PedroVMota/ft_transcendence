// Menu Contnet ('label', 'url', eventListener)

const Menu = [
    ['Home', "/", 'click'],
    ['About', '/about', 'click'],
    ['Contact', '/contact', 'click'],
    ['Login', '/login', 'click'],
    ['Register', '/register', 'click'],
    ['Profile', '/profile', 'click'],
    ['Logout', '/logout', 'click'],
];

document.addEventListener('DOMContentLoaded', function () {

    const navbarMenu = document.getElementById('navbarMenu');

    Menu.forEach(item => {
        const [label, url, event] = item;

        let urlPath = window.location.pathname;


        const listItem = document.createElement('li');
        listItem.className = 'nav-item';

        console.log(`urlPath: ${urlPath}`);
        console.log(`Menu[1]: ${url}`);

        if (urlPath === url) {
            console.log('True');
            listItem.className = 'nav-item active fw-bold';
        } else {
            listItem.className = 'nav-item';
        }

        console.log(listItem.className);

        const link = document.createElement('a');
        link.className = 'nav-link';
        link.href = url;
        link.textContent = label;

        // Add event listener if needed
        if (event === 'click') {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                console.log(`Navigating to ${url}`);
                // Implement your custom logic here
            });
        }

        listItem.appendChild(link);
        navbarMenu.appendChild(listItem);
    });
});
