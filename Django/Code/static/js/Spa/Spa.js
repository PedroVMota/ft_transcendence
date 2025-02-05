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
            console.log(`Matched Profile route with ID: ${profileId}`);
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
            console.error("Footer element not found");
        }

        window.addEventListener('popstate', () => this.loadPage());
    }

    setTo(url) {
        console.log("Navigating to:", url);
        this.#currentRoute?.destroy(); // Clean up the previous route
        this.#currentRoute = null;
    
        // Update history
        window.history.pushState({}, "", window.location.origin + url);
    
        // Match route dynamically
        for (const [route, handler] of this.#routes) {
            console.log("Route:", route);
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
            console.error("No route found for:", url);
        }
    }

    loadPage() {
        try {
            const url = window.location.pathname;
            if (url) {
                this.setTo(url);
            } else {
                console.error("No URL found to load page");
            }
        } catch (error) {
            console.error("Error during loadPage execution:", error);
            
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
            console.error("Root element not found. Unable to reload window.");
        }
    } catch (error) {
        console.error("Error during reloadWindow:", error);
    }
};

export { spa as default, Spa, reloadWindow };