import AComponent from "../Spa/AComponent.js";


export default class Friends extends AComponent {
    #parentElement = null;
    #spaObject = null;

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
    }

    render() {
        let url = this.getUrl();
        // Display pending message
        this.#parentElement.innerHTML = '<span>Pending...</span>';
        this._getHtml(url).then((html) => {
            let documentResponse = new DOMParser().parseFromString(html, 'text/html');
                let rootContentHtml = documentResponse.getElementById('root').innerHTML;
                if(!(!rootContentHtml)){
                    document.head.innerHTML = documentResponse.head.innerHTML;
                    this.#parentElement.innerHTML = rootContentHtml;
                    setTimeout(() => {
                        this.hideSpinner();
                    }, 1000);
                }
            }).catch((error) => {
                
                console.error(error);
            });

    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }
}