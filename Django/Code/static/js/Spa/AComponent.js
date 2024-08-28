import { Requests } from "../Utils/Requests.js";

export default class AComponent{
    #selfUrl;
    #spaObject;
    constructor(url, spaObject){
        if(new.target === AComponent)
            throw new TypeError('Cannot construct abstract instances directly');
        if(this.render === undefined)
            throw new TypeError('You have to implement the method render!');
        this.#selfUrl = url;
        this.#spaObject = spaObject;
    }
    render(){
        throw new Error('You have to implement the method render!');
    }

    async _getHtml(){
        let response = await Requests.get(this.#selfUrl);
        return response;
    }

    getUrl(){
        return this.#selfUrl;
    }

    destroy(){
        throw new Error('You have to implement the method destroy!');
    }

    showSpinner() {
        // Create spinner element
        const spinner = document.createElement('div');
        spinner.className = 'spinner-overlay';
        spinner.innerHTML = `
            <div class="spinner"></div>
        `;
        document.body.appendChild(spinner);
    }

    hideSpinner() {
        const spinner = document.querySelector('.spinner-overlay');
        if (spinner) {
            spinner.remove();
        }
    }

}