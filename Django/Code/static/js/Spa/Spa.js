import Menu from "../Menu/Menu.js";
import Home from "../Home/Home.js";
import Friends from "../Friend/Friends.js";
import Profile from "../profile/profile.js";

class Spa{
    #menu = null;
    #content = null;
    #footer = null;
    #routes = [ "/", "/Profile/", "/Friends/", "/Login/", '/Logout/' ];
    #currentRoute = null;

    constructor(){
        this.#menu = new Menu('/Menu/', this);
        this.#menu.render();
        this.#content = document.getElementById("Content");
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
                this.#currentRoute = new Home(url, this);
                break;
            case "/Profile/":
                this.#updateUrl(url);
                this.#currentRoute = new Profile(url, this);
                break;
            case "/Friends/":
                this.#updateUrl(url);
                this.#currentRoute = new Friends(url, this);
                break;
            case "/Login/":
                this.#updateUrl(url);
                this.#currentRoute = new Login(url, this);
                break;
            case "/Logout/":
                this.#updateUrl(url);
                this.#currentRoute = new Logout(url, this);
                break;
            default:
                console.error("Invalid URL: ", url);
                return;
        }

        this.#currentRoute.render();
    }

    loadPage(){
        console.log("Load Page");
        let url = window.location.pathname;
        this.setTo(url);
    }

    #updateUrl(url){
        window.history.pushState({}, url, window.location.origin + url);
    }

    #isPageReloaded() {
        const [navigationEntry] = performance.getEntriesByType('navigation');
        return navigationEntry && navigationEntry.type === 'reload';
    }

}

const spa = new Spa();


spa.loadPage();



export { spa as default}