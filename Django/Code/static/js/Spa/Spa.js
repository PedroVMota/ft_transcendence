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
                try {
                    const { default: Lobby } = await import("../Lobby/Lobby.js");
                    let lob = new Lobby(url, this, lobbyId);
                    return lob;
                } catch (error) {
                    throw error;
                }
            }.bind(this)],
            [/^\/Game\/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\/?$/, async function (url) {
                const gameId = url.split("/")[2];
                try{
                    const { default: Game } = await import("../Game/Game.js");
                    let gam = new Game(url, this, false, gameId);
                    return gam;
                } catch (error) {
                    throw error;
                }
            }.bind(this)]
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

    async setTo(url) {
        
    
        window.history.pushState({}, "", window.location.origin + url);
    
        for (const [route, handler] of this.#routes) {
            if (typeof route === "string" && route === url) {
                this.#currentRoute = handler();
                break;
            } else if (route instanceof RegExp && route.test(url)) {
                console.log("Matched regex route");
                this.#currentRoute = await handler(url);
         
                break;
            } else {
            }
        }
        console.log("Current route set", this.#currentRoute);
        this.#currentRoute?.destroy(); // Clean up the previous route
    
        try{
            this.#currentRoute?.render();
        }
        catch (error) {
            console.error(error);
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