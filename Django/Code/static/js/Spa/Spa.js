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
    #routes = ["/", "/Profile/", "/Friends/", "/Login/", '/Logout/', '/Game/', /^\/Profile\/\d+$/]; // Add a regex for profile IDs
    #currentRoute = null;
    #contentClass = {
        "/": new Home("/", this),
        "/Profile/": new Profile("/Profile/", this),
        "/Friends/": new Friends("/Friends/", this),
        "/Game/": new Game("/Game/", this),
    };

    constructor() {
        this.#menu = new Menu('/Menu/', this);
        if (!this.#menu) {
            throw new Error("Menu initialization failed");
        }
        else{
            this.#menu.render();
        }

        this.#content = document.getElementById("root");
        if (!this.#content) {
            console.error("Root element not found");
            return;
        }

        this.#footer = document.getElementById("footer");
        if (!this.#footer) {
            console.error("Footer element not found");
            return;
        }

        window.addEventListener('popstate', (event) => {
            this.loadPage();
        });
    }

    setTo(url) {
        console.log("Setting to URL:", url);
        this.#currentRoute?.destroy();
        this.#currentRoute = null;
        window.history.pushState({}, url, window.location.origin + url);
        switch (url) {
            case "/":
                console.log("Setting to Home");
                this.#currentRoute = this.#contentClass["/"];
                break;
            case "/Profile/":
                console.log("Setting to Profile");
                this.#currentRoute = this.#contentClass["/Profile/"];
                break;
            case "/Friends/":
                console.log("Setting to Friends");
                this.#currentRoute = this.#contentClass["/Friends/"];
                break;
            case "/Game/":
                console.log("Setting to Game");
                this.#currentRoute = this.#contentClass["/Game/"];
                break;
            default:
                console.log("CheckAnother Possible routes");
                let isProfileWithId = url.match(/^\/profile\/\d+\/$/i);
                let isLobbyWithId = url.match(/^\/lobby\/\d+\/$/i)
                console.table({
                    "isProfileWithId": isProfileWithId,
                    "url": url
                })
                if (isProfileWithId) {
                    console.log("Setting to Profile with ID");
                    let profileId = url.split("/")[2];
                    this.#currentRoute = new Profile(url, this, false, profileId);
                    this.#currentRoute.render();  // Ensure the render method is called to attach event listeners
                }
                else if (isLobbyWithId)
                {
                    console.log("Setting to Lobby with ID");
                    let lobbyId = url.split("/")[2];
                    this.#currentRoute = new Lobby(url, this, lobbyId);
                    this.#currentRoute.render();
                }
                else {
                    console.error("Unknown URL");
                    return;
                }
                break;
        }
        if (this.#currentRoute) {
            this.#currentRoute.render();
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

export { spa as default };
export { Spa }
export { reloadWindow };
