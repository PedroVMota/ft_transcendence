import Menu from "../Menu/Menu.js";
import Home from "../Home/Home.js";
import Friends from "../Friend/Friends.js";
import Profile from "../profile/profile.js";
import Game from "../Game/Game.js";

class Spa {
    #menu = null;
    #content = null;
    #footer = null;
    #currentRoute = null;

    // Routes as a Map for easier handling
    #routes = null;

    constructor() {
        this.#routes = new Map([
            ["/", () => new Home("/", this)],
            ["/Profile/", () => new Profile("/Profile/", this)],
            ["/Friends/", () => new Friends("/Friends/", this)],
            ["/Game/", () => new Game("/Game/", this)],
            [/^\/Profile\/\d+\/?$/, (url) => {
                const profileId = url.split("/")[2];
                return new Profile(url, this, false, profileId);
            }],
            [/^\/Lobby\/[0-9a-fA-F-]{36}\/?$/, async function (url) {
                const lobbyId = url.split("/")[2];
                console.log("Creating Lobby instance with ID:", lobbyId);
                try {
                    const { default: Lobby } = await import("../Lobby/Lobby.js");
                    let lob = new Lobby(url, this, lobbyId);
                    console.log("Lobby instance created:", lob);
                    return lob;
                } catch (error) {
                    console.error("Error creating Lobby instance:", error);
                    throw error;
                }
            }.bind(this)],
            [/^\/Game\/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\/?$/, (url) => {
                const gameId = url.split("/")[2];
                return new Game(url, this, false, gameId);
            }]
        ]);

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
    
        window.history.pushState({}, "", window.location.origin + url);
    
        for (const [route, handler] of this.#routes) {
            if (typeof route === "string" && route === url) {
                console.log("Matched exact route:", route);
                this.#currentRoute = handler();
                break;
            } else if (route instanceof RegExp && route.test(url)) {
                console.log("Matched regex route:", route);
                this.#currentRoute = handler(url);
                console.log("Handler:", handler);
                console.log("Current Route:", this.#currentRoute);
                break;
            } else {
                console.log("Route not matched:", route);
            }
        }
    
        if (this.#currentRoute) {
            console.log("About to render current route.");
            this.#currentRoute.render();
        } else {
            console.error("Handler did not return a valid component instance.");
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