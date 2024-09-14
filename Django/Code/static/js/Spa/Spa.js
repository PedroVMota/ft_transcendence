import Menu from "../Menu/Menu.js";
import Home from "../Home/Home.js";
import Friends from "../Friend/Friends.js";
import Profile from "../profile/profile.js";
import Game from "../Game/Game.js";



class Spa{
    #menu = null;
    #content = null;
    #footer = null;
    #routes = [ "/", "/Profile/", "/Friends/", "/Login/", '/Logout/', '/Game/' ];
    #currentRoute = null;
    #contentClass = {
        "/": new Home("/", this),
        "/Profile/": new Profile("/Profile/", this),
        "/Friends/": new Friends("/Friends/", this),
        "/Game/": new Game("/Game/", this),
    }

    constructor(){
        // https://wallpapercave.com/wp/wp3837751.jpg
        this.#menu = new Menu('/Menu/', this);
        this.#menu.render();
        this.#content = document.getElementById("root");
        this.#footer = document.getElementById("Footer");
        
    }

    setTo(url){
        if(!this.#routes.includes(url)){
            console.error("Invalid URL: ", url);
            return;
        }
        if(this.#currentRoute){
            this.#currentRoute.destroy();
        }
        switch(url){
            case "/":
                this.#updateUrl(url);
                this.#currentRoute = this.#contentClass["/"];
                break;
            case "/Profile/":
                this.#updateUrl(url);
                this.#currentRoute = this.#contentClass["/Profile/"];
                break;
            case "/Friends/":
                this.#updateUrl(url);
                this.#currentRoute = this.#contentClass["/Friends/"];
                break;
            case "/Game/":
                this.#updateUrl(url);
                this.#currentRoute = this.#contentClass["/Game/"];
                break;
            default:
                console.error("Invalid URL: ", url);
                return;
        }
        this.#currentRoute.render();
    }

    loadPage(){
        console.log("Load Page teste pedro");
        let url = window.location.pathname;
        this.setTo(url);
    }

    #updateUrl(url){
        window.history.pushState({}, url, window.location.origin + url);
    }
}

const spa = new Spa();

export { spa as default}