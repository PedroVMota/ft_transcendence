import Menu from "../Menu/Menu.js";
import Home from "../Home/Home.js";
import Friends from "../Friend/Friends.js";
import Profile from "../profile/profile.js";
import Game from "../Game/Game.js";
import Lobby from "../Lobby/Lobby.js"

class Spa {
    #menu = null;
    #content = null;
    #footer = null;
    #currentRoute = null;

    // Routes as a Map for easier handling
    #routes = new Map([
        ["/", () => new Home("/", this)],
        ["/Profile/", () => new Profile("/Profile/", this)],
        ["/Friends/", () => new Friends("/Friends/", this)],
        ["/Game/", () => new Game("/Game/", this)],
        [/^\/Profile\/\d+\/?$/, (url) => {
            const profileId = url.split("/")[2];
            return new Profile(url, this, false, profileId);
        }],
        [/^\/Lobby\/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\/?$/, (url) => {
            const lobbyId = url.split("/")[2];
            return new Lobby(url, this, lobbyId);
        }],
        [/^\/Game\/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\/?$/, (url) => {
            const gameId = url.split("/")[2];
            return new Game(url, this, false, gameId);
        }]
    ]);

    constructor() {
        this.#menu = new Menu('/Menu/', this);
        if (!this.#menu) {
            throw new Error("Menu initialization failed");
        } else {
            this.#menu.render();
        }

        this.#content = document.getElementById("root");
        if (!this.#content) {
            throw new Error("Root element not found");
        }

        this.#footer = document.getElementById("footer");
        if (!this.#footer) {
        }

        window.addEventListener('popstate', () => this.loadPage());
    }

    setTo(url) {
        this.#currentRoute?.destroy(); // Clean up the previous route
        this.#currentRoute = null;
    
        // Update history
        window.history.pushState({}, "", window.location.origin + url);
    
        // Match route dynamically
        for (const [route, handler] of this.#routes) {
            if (typeof route === "string" && route === url) {
                this.#currentRoute = handler();
                break;
            } else if (route instanceof RegExp && route.test(url)) {
                this.#currentRoute = handler(url);
                break;
            }
        }
    
        if (this.#currentRoute) {
            this.#currentRoute.render(); // Render the matched route
        } else {
        }
    }

    loadPage() {
        try {
            const url = window.location.pathname;
            if (url) {
                this.setTo(url);
            } else {
            }
        } catch (error) {
            
        }
    }
}

const spa = new Spa();
spa.loadPage();

const reloadWindow = () => {
    try {
        const root = document.getElementById("root");
        if (root) {
            root.innerHTML = "";
            spa.loadPage();
        } else {
        }
    } catch (error) {
    }
};

export { spa as default, Spa, reloadWindow };