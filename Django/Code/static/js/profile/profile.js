import AComponent from "../Spa/AComponent.js";
import spa from "../Spa/Spa.js";
import { getCookie, Requests } from "../Utils/Requests.js";


export default class Profile extends AComponent {
    #parentElement = null;
    #spaObject = null;
    #cachedContent = null;
    #cachedHead = null;

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
    }

    render() {
        if(this.#cachedContent){
            document.head.innerHTML = this.#cachedHead;
            this.#parentElement.innerHTML = this.#cachedContent;
            document.getElementById('profileForm').addEventListener('submit', (event) => this.#updateProfile(event));
            this.#loadData();
            return;
        }
        let url = this.getUrl();
        // Display pending message
        this.showSpinner();
        this._getHtml(url).then((html) => {
            console.log('=> Profile: ', html);
        let documentResponse = new DOMParser().parseFromString(html, 'text/html');
            let rootContentHtml = documentResponse.getElementById('root').innerHTML;
            if(!(!rootContentHtml)){
                document.head.innerHTML = documentResponse.head.innerHTML;
                this.#parentElement.innerHTML = rootContentHtml;
                document.getElementById('profileForm').addEventListener('submit', (event) => this.#updateProfile(event));
                this.#loadData();
                setTimeout(() => {
                    this.hideSpinner();
                }, 1000);
                this.#cachedContent = rootContentHtml;
                this.#cachedHead = documentResponse.head.innerHTML;
            }
        }).catch((error) => {
            console.error(error);
        });
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

    #loadData() {

        Requests.get('/getUserData/').then((userData) => {
            // userData = userData.user;
            document.getElementById('id_first_name').value = userData.user.first_name ? userData.user.first_name : 'Empty';
            document.getElementById('id_last_name').value = userData.user.last_name ? userData.user.last_name : 'Empty';
            document.getElementById('id_about_me').value = userData.user.about_me ? userData.user.about_me : 'Empty';
            document.getElementById('profilePicture').src = userData.user.profile_picture;
            document.getElementById('id_user_code').value = userData.user.usercode;
        })
    }

    #updateProfile(event) {
        event.preventDefault();
        const formData = new FormData(document.getElementById('profileForm'));
        fetch('/Profile/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    this.#loadData();
                } else if (data.error) {
                    alert('Error updating profile: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error during fetch:', error);
                alert('An error occurred. Please try again.');
            });
    }
}

