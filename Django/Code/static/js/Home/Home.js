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
        const url = this.getUrl()
        if(this.#parentElement.innerHTML !== ''){
            return ;
        }
        this._getHtml(url).then((html) => {
            let doomResponse = new DOMParser().parseFromString(html, 'text/html');
            let rootContentHtml = doomResponse.getElementById('root').innerHTML;
            if (rootContentHtml) {
                document.head.innerHTML = doomResponse.head.innerHTML;
                this.#parentElement.innerHTML = rootContentHtml;
            }
            else {
                null
            }
        }).catch((error) => {
            console.error('Error fetching HTML:', error);
        });
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }
}