import AComponent from "../Spa/AComponent.js";
import { Requests, getCookie } from "../Utils/Requests.js";

class Menu extends AComponent {
    #parentElement = null;
    #spaObject = null;

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("headerMenu");
        this.#spaObject = spaObject;
    }

    render() {
        let url = this.getUrl();
        this._getHtml(url).then((html) => {
            // this.#parentElement.innerHTML = html;
            // let home = document.getElementById("nav-home");
            let profile = document.getElementById("nav-profile");
            let friends = document.getElementById("nav-friends");
            let logout = document.getElementById("nav-logout");
            // there are two elements with the same id to get the use all the elements with the same id
            let home = document.querySelectorAll("#nav-home");

            // home.addEventListener("click", (e) => this.navigateTo(e, "/"));
            home.forEach((element) => {
                element.addEventListener("click", (e) => this.navigateTo(e, "/"));
            });
            profile.addEventListener("click", (e) => this.navigateTo(e, "/Profile/"));
            friends.addEventListener("click", (e) => this.navigateTo(e, "/Friends/"));
            logout.addEventListener("click", (e) => this.#logout(e));
        }).catch((error) => {
            console.error(error);
        });
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

    async #logout(e) {
        e.preventDefault();
        const Header = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
        const rep = await Requests.post('/Logout/', {}, Header);
        console.log(rep);
        // window.location.href = '/';
    }

    navigateTo(e, url) {
        e.preventDefault();
        console.log("Navigate to: ", url);
        console.log("SPA Object: ", this.#spaObject);
        this.#spaObject.setTo(url);
    }
}

export default Menu;