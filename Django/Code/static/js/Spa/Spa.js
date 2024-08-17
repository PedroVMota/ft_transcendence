import Requests from '../Utils/Requests.js';
import Menu from '../Menu/index.js';

/**
 * Retrieves the value of a specified cookie.
 * @param {string} name - The name of the cookie.
 * @returns {string|null} The value of the cookie, or null if not found.
 */
function GetCookie(name) {
    const cookieList = document.cookie.split(";");
    for (const cookie of cookieList) {
        const [cookieName, cookieValue] = cookie.split("=").map(c => c.trim());
        if (cookieName === name) return cookieValue;
    }
    return null;
}

const STATUS = { "HOME": 0, "PROFILE": 1, "LOGIN": 2, "LOGOUT": 3, "FRIENDS": 4 };

/**
 * Spa class to handle single-page application operations.
 */
class Spa {
    #status = STATUS.LOGIN;
    #user = null;
    #accessToken = null;
    #refreshToken = null;
    #body = null;
    #Menu = null;
    #spaBody = null;

    /**
     * Creates a Spa object.
     */
    constructor() {
        console.log("Spa object created");
        this.#body = document.querySelector("body");

        const accessToken = GetCookie("access");
        const refreshToken = GetCookie("refresh");
        if (accessToken && refreshToken) {
            this.#accessToken = accessToken;
            this.#refreshToken = refreshToken;
            console.log("User logged in");
        }

        this.#Menu = new Menu(this.#body, this);
        this.#Menu.init();

        this.#spaBody = this.createDiv("SpaBody");
        this.#body.appendChild(this.#spaBody);
    }

    /**
     * Creates a div element with optional id and classes.
     * @param {string|null} id - The id of the div.
     * @param {Array<string>} classes - The classes to add to the div.
     * @returns {HTMLDivElement} The created div element.
     */
    createDiv(id = null, classes = []) {
        const div = document.createElement("div");
        if (id) div.id = id;
        if (classes.length > 0) div.classList.add(...classes);
        return div;
    }

    /**
     * Translates a URL to a status.
     * @param {string} url - The URL to translate.
     * @returns {number} The corresponding status.
     */
    #translationUrlToStatus(url) {
        const urlPreset = ["/", "/Profile/", "/Login/", "/Logout/", "/Friends/"];
        const statusPreset = [STATUS.HOME, STATUS.PROFILE, STATUS.LOGIN, STATUS.LOGOUT, STATUS.FRIENDS];
        const index = urlPreset.indexOf(url);
        if (index !== -1) {
            console.log(`Url: ${url} Status: ${statusPreset[index]}`);
            return statusPreset[index];
        }
    }

    /**
     * Updates the page content based on the current status.
     */
    async #updatePage() {
        const content = {
            [STATUS.HOME]: "<h1>Home</h1>",
            [STATUS.PROFILE]: "<h1>Profile</h1>",
            [STATUS.LOGIN]: "<h1>Login</h1>",
            [STATUS.LOGOUT]: "<h1>Logout</h1>",
            [STATUS.FRIENDS]: "<h1>Friends</h1>",
        }[this.#status] || "<h1>404</h1>";

        this.#cleanSpaBody();
        this.#spaBody.innerHTML = content;
    }

    /**
     * Navigates to a specified URL.
     * @param {string} url - The URL to navigate to.
     */
    async get(url) {
        window.history.pushState({}, '', url);
        this.#status = this.#translationUrlToStatus(url);
        console.log("Status: ", this.#status);
        if (this.#status !== undefined && this.#status !== null) {
            this.#updatePage();
        }
    }

    /**
     * Sets the status based on the current URL.
     */
    setStatus() {
        const url = window.location.pathname;
        this.#status = this.#translationUrlToStatus(url);
        console.log("Status: ", this.#status);
        if (this.#status !== undefined && this.#status !== null) {
            this.#updatePage();
        }
    }

    /**
     * Cleans the Spa body by removing all its children.
     */
    #cleanSpaBody() {
        this.#spaBody.innerHTML = '';
    }
}

const route = new Spa();

// Handle back/forward browser button clicks
window.addEventListener('popstate', () => {
    // route.setStatus();
});

export { route, GetCookie, Spa, STATUS };