function GetCookie(name) {
    let cookie = document.cookie;
    let cookieList = cookie.split(";");
    for (let i = 0; i < cookieList.length; i++) {
        let cookieName = cookieList[i].split("=")[0].trim();
        let cookieValue = cookieList[i].split("=")[1].trim();
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
}
const STATUS = {
    "HOME": 0,
    "PROFILE": 1,
    "LOGIN": 2,
    "LOGOUT": 3
};
export class Spa {
    #status = STATUS.LOGIN;
    #user = null;
    #accessToken = null;
    #refreshToken = null;
    #body = null;

    constructor() {
        console.log("Spa object created");
        this.#status = STATUS.LOGIN;
        this.#user = null;
        this.#accessToken = null;
        this.#refreshToken = null;
        this.#body = document.querySelector("body");

        if (GetCookie("access") !== null && GetCookie("refresh") !== null) {
            this.#accessToken = GetCookie("access");
            this.#refreshToken = GetCookie("refresh");
            console.log("User logged in");
        }

        this.setStatus();
    }

    async #fetchGet(url) {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'authorization': 'Bearer ' + this.#accessToken
            }
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); // Return the HTML content as text
    }

    #translationUrlToStatus(url) {
        switch (url) {
            case '/':
                return STATUS.HOME;
            case '/Profile/':
                return STATUS.PROFILE;
            case '/Logout/':
                return STATUS.LOGOUT;
            default:
                return null;
        }
    }

    async #updatePage() {
        console.log("Update Page");
        switch (this.#status) {
            case STATUS.HOME:
                await this.#setMenu();
                break;
            case STATUS.PROFILE:
                this.#body.innerHTML = "<h1>Profile</h1>";
                break;
            case STATUS.LOGOUT:
                this.#body.innerHTML = "<h1>Logout</h1>";
                break;
            default:
                this.#body.innerHTML = "<h1>404 Not Found</h1>";
                break;
        }
    }

    async #setMenu() {
        let url = "/Menu/";
        let response = await this.#fetchGet(url);
        this.#body.innerHTML = response;
        this.#jsMenu();
    }

    async get(url) {
        // Update the browser history and status
        window.history.pushState({}, '', url);
        this.#status = this.#translationUrlToStatus(url);

        if (this.#status !== null) {
            await this.#updatePage();
        }
    }

    setStatus() {
        let currentUrl = window.location.pathname;
        console.log("Current URL:", currentUrl);
        let newStatus = this.#translationUrlToStatus(currentUrl);
        console.log("New Status:", newStatus);

        if (newStatus !== null) {
            this.#status = newStatus;
            this.get(currentUrl);
        }
    }

    #jsMenu() {
        let menuToggler = document.getElementById("MenuToggler");
        let closeMenu = document.getElementById("CloseMenu");
        let menuScreenBlur = document.getElementById("MenuScreenBlur");
        let navHome = document.getElementById("nav-home");
        let navProfile = document.getElementById("nav-profile");

        if (menuToggler) {
            menuToggler.addEventListener("click", function (e) {
                e.preventDefault();
                document.getElementById("MenuItems").style.transform = "translateX(0)";
                document.getElementById("MenuScreenBlur").classList.remove("d-none");
            });
        }
        if (closeMenu) {
            closeMenu.addEventListener("click", function (e) {
                e.preventDefault();
                document.getElementById("MenuItems").style.transform = "translateX(-100%)";
                document.getElementById("MenuScreenBlur").classList.add("d-none");
            });
        }

        if (menuScreenBlur) {
            menuScreenBlur.addEventListener("click", function (e) {
                e.preventDefault();
                document.getElementById("MenuItems").style.transform = "translateX(-100%)";
                document.getElementById("MenuScreenBlur").classList.add("d-none");
            });
        }

        if (navHome) {
            navHome.addEventListener("click", (e) => {
                e.preventDefault();
                this.get("/"); // Load the home page via SPA
            });
        }
        if (navProfile) {
            navProfile.addEventListener("click", (e) => {
                e.preventDefault();
                this.get("/Profile/"); // Load the profile page via SPA
            });
        }
    }

    #emptyHtml() {
        this.#body.innerHTML = "";
    }
}

const spa = new Spa();

// Handle back/forward browser button clicks
window.addEventListener('popstate', () => {
    spa.setStatus();
});


