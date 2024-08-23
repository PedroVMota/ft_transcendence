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

function checyAnyKindaUndefined(value, msgAlert) {
    let isUndefined = false;
    if (value === undefined) {
        isUndefined = true;
    }
    if(isUndefined) {
        console.trace()
        console.alert(msgAlert);
    }
}

/**
 * Removes a cookie by setting its expiration date to the past.
 * @param {string} name - The name of the cookie to remove.
 */
function removeCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${window.location.hostname}; secure=true;`;
    console.log(`Cookie '${name}' has been removed.`);
}


const STATUS = { "HOME": 0, "PROFILE": 1, "LOGIN": 2, "LOGOUT": 3, "FRIENDS": 4 };

/**
 * Spa class to handle single-page application operations.
 */
class Spa {
    #status = STATUS.LOGIN;
    #body = null;
    #Menu = null;
    #BMenu = null;
    #spaBody = null;

    /**
     * Creates a Spa object.
     */
    constructor() {
        console.log("Spa object created");
        
        this.#body = document.querySelector("body");

        this.#BMenu = this.createDiv("MenuBody");
        document.querySelector("body").appendChild(this.#BMenu);

        this.#Menu = new Menu(this.#BMenu, this);
        this.#Menu.init();

        this.#spaBody = this.createDiv("SpaBody");
        this.#spaBody.classList.add("px-4");
        this.#body.appendChild(this.#spaBody);
        

        this.#updatePage();
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
        if(url === "/") return STATUS.HOME;
        if(url === "/Profile/") return STATUS.PROFILE;
        if(url === "/friends/") return STATUS.FRIENDS;
        if(url === "/logout/") return STATUS.LOGOUT;
        return STATUS.LOGIN;
    }

    /**
     * Updates the page content based on the current status.
     */
    async #updatePage() {
        this.#status = this.#translationUrlToStatus(window.location.pathname);
        switch (this.#status) {
            case STATUS.HOME:
                console.log("Home page");
                this.#cleanSpaBody();
                

                break;
            case STATUS.PROFILE:
                console.log("Profile page");
                await Requests.get('/Profile/').then((html) => {
                    this.#cleanSpaBody();
                    this.#spaBody.innerHTML = html;
                }).catch((error) => {
                    console.error(error);
                }
                );
                break;
            default:
                break;
        }
    }

    /**
     * Navigates to a specified URL.
     * @param {string} url - The URL to navigate to.
     */
    async get(url) {
        window.history.pushState({}, '', url);
        this.#status = this.#translationUrlToStatus(url);
        this.#updatePage();
    }
    /**
     * Sets the status based on the current URL.
     */
    setStatus() {
        const url = window.location.pathname;
        this.#status = this.#translationUrlToStatus(url);
        this.#updatePage();
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
    route.setStatus();
});

export { GetCookie, removeCookie, Spa, STATUS , route, checyAnyKindaUndefined};