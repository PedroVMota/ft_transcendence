import Requests from "../Utils/Requests.js";
import { route as spa, GetCookie } from "../Spa/Spa.js";

/**
 * Menu class to handle menu operations.
 */
export default class Menu {
    /**
     * Creates a Menu object.
     * @param {HTMLElement} parentelement - The parent element to attach the menu.
     * @param {Object} spa - The SPA instance.
     */

    /**
     * Initializes the menu by loading it and attaching event listeners.
     */
    constructor(){
        this.init();
    }
    async init() {
        this.attachEventListeners();
    }

    /**
     * Loads the menu content from the server.
     */
    /**
     * Attaches event listeners to menu elements.
     */
    attachEventListeners() {
        const events = [
            { id: "MenuToggler", event: "click", handler: this.openMenu.bind(this) },
            { id: "CloseMenu", event: "click", handler: this.closeMenu.bind(this) },
            { id: "MenuScreenBlur", event: "click", handler: this.closeMenu.bind(this) },
            { id: "nav-home", event: "click", handler: (e) => this.navigateTo(e, "/") },
            { id: "nav-profile", event: "click", handler: (e) => this.navigateTo(e, "/Profile/") },
            { id: "nav-friends", event: "click", handler: (e) => this.navigateTo(e, "/Friends/") },
            { id: "nav-logout", event: "click", handler: (e) => this.#logout(e) }
        ];

        events.forEach(({ id, event, handler }) => {
            const element = document.getElementById(id);
            if (element) element.addEventListener(event, handler);
        });
    }

    /**
     * Opens the menu.
     * @param {Event} e - The event object.
     */
    openMenu(e) {
        e.preventDefault();
        this.toggleMenu("translateX(0)", false);
    }

    /**
     * Closes the menu.
     * @param {Event} e - The event object.
     */
    closeMenu(e) {
        e.preventDefault();
        this.toggleMenu("translateX(-100%)", true);
    }

    /**
     * Toggles the menu visibility.
     * @param {string} transform - The transform style for the menu.
     * @param {boolean} hideBlur - Whether to hide the blur effect.
     */
    toggleMenu(transform, hideBlur) {
        const menuItems = document.getElementById("MenuItems");
        const menuScreenBlur = document.getElementById("MenuScreenBlur");
        if (menuItems) menuItems.style.transform = transform;
        if (menuScreenBlur) menuScreenBlur.classList.toggle("d-none", hideBlur);
    }

    /**
 * Navigates to a specified URL.
 * @param {Event|null} e - The event object, or null if no event.
 * @param {string} url - The URL to navigate to.
 */
    navigateTo(e, url) {
        
        if (e && typeof e.preventDefault === 'function') {
            e.preventDefault();
        }
        if (typeof spa !== "undefined") {
            spa.get(url);
            this.closeMenu(new Event("click"));
        } else {
            console.error("Spa instance not available");
        }
    }

   async #logout(e) {
        e.preventDefault();
        const Header = {
            'Content-Type': 'application/json',
            'X-CSRFToken': GetCookie('csrftoken')
        }
        const rep = await Requests.post('/Logout/', {}, Header);
        console.log(rep);
        window.location.href = '/';
    }

}