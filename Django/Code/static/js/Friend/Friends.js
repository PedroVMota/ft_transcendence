import AComponent from "../Spa/AComponent.js";


export default class Friends extends AComponent {
    #parentElement = null;
    #spaObject = null;

    constructor(url, spaObject) {
        super(url, spaObject);
        console.log("Friend constructor");
        this.#parentElement = document.getElementById("root");
        console.log(">>>> Spa Object: ", spaObject);
        this.#spaObject = spaObject;
        console.trace({
            "Parent Element": this.#parentElement
        });
    }

    render() {
        console.trace("Render Friends");
        let url = this.getUrl();
        // Display pending message
        this.#parentElement.innerHTML = '<span>Pending...</span>';
        this._getHtml(url).then((html) => {
            this.#parentElement.innerHTML = html;
        }).catch((error) => {
            console.error(error);
        });

    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }
}