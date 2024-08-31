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



let isScrolling;

document.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const scrollFactor = scrollTop / (document.body.scrollHeight - window.innerHeight);

    const backgroundPositionY = scrollFactor * 2; // Adjust for desired parallax effect

    const styleElement = document.querySelector('#dynamic-style') || document.createElement('style');
    styleElement.id = 'dynamic-style';

    // Add blur while scrolling
    styleElement.textContent = `
        .backgroundBody::before {
            background-position-y: ${backgroundPositionY}%;
            filter: blur(3px); /* Apply blur when scrolling */
            transition: filter 0.3s ease-out; /* Smooth transition for removing blur */
        }
    `;

    console.log(styleElement.textContent);

    document.head.appendChild(styleElement);

    // Clear the timeout if it's already set
    window.clearTimeout(isScrolling);

    // Set a timeout to remove the blur class after scrolling has stopped
    isScrolling = setTimeout(() => {
        styleElement.textContent = `
            .backgroundBody::before {
                background-position-y: ${backgroundPositionY}%;
                filter: blur(0px); /* Remove blur after scrolling stops */
                transition: filter 0.3s ease-out; /* Smooth transition */
            }
        `;
        document.head.appendChild(styleElement);
    }, 150); // Adjust this timeout to control how quickly the blur is removed after scrolling stops
});


spa.loadPage();


export { spa as default}