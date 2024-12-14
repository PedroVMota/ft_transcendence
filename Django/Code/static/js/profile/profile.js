import AComponent from "../Spa/AComponent.js";
import spa, { reloadWindow } from "../Spa/Spa.js";
import { getCookie } from "../Utils/Requests.js";

export default class Profile extends AComponent {
    #parentElement = null;
    #spaObject = null;
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
        console.log("Rendering Profile");

        // If the parent already has content, just attach event listeners again.
        if (this.#parentElement.innerHTML !== '') {
            console.log("Parent element not empty");
            this.#attachEventListeners();
            return;
        }

        const url = this.getUrl();

        // Fetch the HTML first
        this._getHtml(url)
            .then((html) => {
                const newDom = new DOMParser().parseFromString(html, 'text/html');

                const root = newDom.getElementById("root");
                if (!root) {
                    console.error("Root not found in fetched HTML");
                    return;
                }

                this.#parentElement.innerHTML = root.innerHTML;

                // Now that the HTML is in place, attach event listeners
                this.#attachEventListeners();
            })
            .catch((error) => {
                console.error("Error fetching HTML:", error);
            });
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

    #attachEventListeners = () => {
        console.log(`Attaching event listeners for profile ${this.#profileId} with myProfile = ${this.#myProfile}`);

        // If the profile is not mine, enable add/remove friend features
        if (!this.#myProfile) {
            console.log("Profile is not mine");
            this.#enableAddFriend();
            this.#enableRemoveFriend();
        }

        // If edit profile form exists, enable profile editing
        this.#enableEditProfile();
    }

    #enableAddFriend = () => {
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

    #enableEditProfile = () => {
        const editProfileForm = document.getElementById('editProfileForm');
        if (!editProfileForm) return;

        editProfileForm.addEventListener('submit', (e) => {
            e.preventDefault();

            let formData = new FormData();
            formData.append('first_name', document.getElementById('first_name').value);
            formData.append('last_name', document.getElementById('last_name').value);

            const profilePicture = document.getElementById('profile_picture').files[0];
            const profileBanner = document.getElementById('profile_banner').files[0];
            if (profilePicture) formData.append('profile_picture', profilePicture);
            if (profileBanner) formData.append('profile_banner', profileBanner);

            fetch('/Auth/token/user/update/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message === 'User updated successfully.') {
                        alert(data.message);

                        let modalElement = document.getElementById('editProfileModal');
                        let modal = bootstrap.Modal.getInstance(modalElement);
                        modal.hide();

                        modalElement.addEventListener('hidden.bs.modal', () => {
                            document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
                            reloadWindow();
                        });
                    } else {
                        alert(data.error || 'Failed to update profile');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while updating the profile');
                });
        });
    }
}
