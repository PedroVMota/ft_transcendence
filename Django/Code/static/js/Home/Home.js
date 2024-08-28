import AComponent from "../Spa/AComponent.js";


export default class Home extends AComponent {
    #parentElement = null;
    #spaObject = null;

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
    }

    render() {
        // let url = this.getUrl();
        // // Display pending message
        // this.#parentElement.innerHTML = '<span>Pending...</span>';

        // this._getHtml(url).then((html) => {
        //     console.log("HTML: ", html);
        //     this.#parentElement.innerHTML = html;
        // }).catch((error) => {
        //     console.error(error);
        // });

        this.#parentElement.innerHTML = '<h1>Home</h1>';
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }
}