import AComponent from "../Spa/AComponent.js";
import spa, { reloadWindow } from "../Spa/Spa.js";
import { getCookie, Requests } from "../Utils/Requests.js";


export default class Profile extends AComponent {
    #parentElement = null;
    #spaObject = null;
    #cachedContent = null;
    #cachedHead = null;
    #myProfile = true;
    #profileId = null;

    constructor(url, spaObject, myProfile = true, profileId = null) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
        this.#myProfile = myProfile;
        this.#profileId = profileId;
    }
    render() {
        if(this.#parentElement.innerHTML !== '') {
            console.log("Parent element not empty");
            this.#attachEventListeners();
            return;
        }

        console.log("Rendering Profile");
        let url = this.getUrl();
        this._getHtml(url).then((html) => {
            let newDom = new DOMParser().parseFromString(html, 'text/html');
            document.head.innerHTML = newDom.head.innerHTML;

            let root = newDom.getElementById("root");
            if(!root) {
                console.error("Root not found");
                return;
            }
            this.#parentElement.innerHTML = root.innerHTML;
            this.#attachEventListeners();

        });
    }
    
    destroy() {
        this.#parentElement.innerHTML = '';
    }

    #attachEventListeners = () => {
        console.log(`Attaching event listeners for profile ${this.#profileId} with myProfile = ${this.#myProfile}`);
        if(!this.#myProfile) {

            console.log("Profile is not mine");
            this.#enableAddFriend();
            this.#enableRemoveFriend();
        }
    }

    #enableAddFriend = () => {
        // Add event listener for "Add Friend" button
        const addFriendButton = document.getElementById('addFriendButton');
        if (addFriendButton) {
            console.log('Add friend button found');
            addFriendButton.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Add friend button clicked');
                const url = `/auth/token/friend/request/send/`;
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ user_code: this.#profileId })
                })
                .then(response => {
                    if (response.ok) {
                        alert('Friend request sent');
                        reloadWindow();
                    } else {
                        alert('Failed to send friend request');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        }
    }

    #enableRemoveFriend = () => {
        // Add event listener for "Remove Friend" button
        const removeFriendButton = document.getElementById('removeFriendButton');
        if (removeFriendButton) {
            console.log('Remove friend button found');
            removeFriendButton.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Remove friend button clicked');
                const url = `/auth/token/remove/${this.#profileId}/`;
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => {
                    if (response.ok) {
                        alert('Friend removed');
                        reloadWindow();
                    } else {
                        alert('Failed to cancel friend request');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        }
    }
}