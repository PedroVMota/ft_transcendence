import AComponent from "../Spa/AComponent.js";
import { Requests, getCookie } from "../Utils/Requests.js";

const CONSTANTS = {
    URLS: {
        FRIEND_REQUEST: '/auth/token/friend/request/manage/',
        INVITE_MANAGE: '/auth/token/invite/manage/',
        FRIEND_REQUEST_GET: '/auth/token/friend/request/get/'
    },
    CLASSES: {
        HIDDEN: 'd-none'
    }
};
    

class Menu extends AComponent {
    #parentElement = null;
    #spaObject = null;
    #numberofNotifications = 0;
    #numberofMessages = 0;
    #notificationSocket = null;
    #defaultHeader =
        {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        };
    #showNotifications = false;
    #deployNotifications = false;



    watchNotifications = () => {
        let notificationsDropdown = document.getElementById("notificationsDropdown");
        let notificationsMenu = document.getElementById("notificationsMenu");
        if (notificationsDropdown === null || notificationsMenu === null) {
            return;
        } else {
            setInterval(() => {
                if (this.#showNotifications) {
                    notificationsMenu.style.display = "block";
                } else {
                    notificationsMenu.style.display = "none";
                }
            }, 500);
        }
    }

    // Increase the number of notifications or messages
    IncreaseNotificationCount = (Target, event) => {
        if (event === "notifications") this.#numberofNotifications += 1;
        else if (event === "message") this.#numberofMessages += 1;
        this.#decoratorToggle();
    }
    // Decrease the number of notifications or messages
    DecrementNotificationCount = (Target, event) => {
        if (event === "notifications") this.#numberofNotifications -= 1;
        else if (event === "message") this.#numberofMessages -= 1;
        this.#decoratorToggle();
    }
    // Check if the element has the class
    #doesHtmlHasClass = (element, className) => {
        return element.classList.contains(className);
    }
    // Decorator to toggle the notification badge
    #decoratorToggle() {
        let notificationBadge = document.getElementById("notificationBadge");
        let messagesBadge = document.getElementById("messagesBadge");
        if (notificationBadge === null || messagesBadge === null)
            return;
        if (this.#numberofNotifications > 0) {
            if (this.#doesHtmlHasClass(notificationBadge, CONSTANTS.CLASSES.HIDDEN))
                notificationBadge.classList.remove(CONSTANTS.CLASSES.HIDDEN);
            notificationBadge.innerText = this.#numberofNotifications;
        }
        else {
            if (!this.#doesHtmlHasClass(notificationBadge, CONSTANTS.CLASSES.HIDDEN))
                notificationBadge.classList.add(CONSTANTS.CLASSES.HIDDEN);
        }

        if (this.#numberofMessages > 0) {
            if (this.#doesHtmlHasClass(messagesBadge, CONSTANTS.CLASSES.HIDDEN))
                messagesBadge.classList.remove(CONSTANTS.CLASSES.HIDDEN);
            messagesBadge.innerText = this.#numberofMessages;
        }
        else {
            if (!this.#doesHtmlHasClass(messagesBadge, CONSTANTS.CLASSES.HIDDEN))
                messagesBadge.classList.add(CONSTANTS.CLASSES.HIDDEN);
        }
    }

    #renderFriendRequests = (data) => {
        let notificationsList = document.getElementById("notificationsMenu");
        let notificationBadge = document.getElementById("notificationBadge");

        if(notificationBadge === null || notificationsList === null) { return; }
    
        if (data.friend_requests === undefined || data.friend_requests.length === 0) {
            notificationsList.innerHTML = `<li><span class="dropdown-item-text">No new notifications</span></li>`;
            notificationBadge.textContent = '0';
        } else {
            notificationBadge.textContent = data.friend_requests.length;
            notificationsList.innerHTML = ''; // Clear existing notifications
            data.friend_requests.forEach((friendRequest) => {
                if(friendRequest.request_type === "friend_request"){
                    let notification = document.createElement('a');
                    notification.classList.add('dropdown-item');
                    notification.href = '#';
                    notification.innerHTML = `
                        <div class="d-flex align-items-center" data-idrequest="${friendRequest.request_id}">
                            <div class="py-1 px-1">
                                <img class="rounded-circle" src="${friendRequest.from_user_profile_picture}" width="50" height="50" alt="Profile Picture">
                            </div>
                            <div class="flex-grow-1 px-1">
                                <div class="font-weight-bold">${friendRequest.from_user}</div>
                                <div class="text-muted small">sent you a friend request.</div>
                                <div class="mt-2">
                                    <button class="btn btn-success btn-sm mr-2" id="acceptRequest_${friendRequest.request_id}" data-request="${friendRequest.request_id}">Accept</button>
                                    <button class="btn btn-danger btn-sm" id="denyRequest_${friendRequest.request_id}" data-request="${friendRequest.request_id}">Deny</button>
                                </div>
                            </div>
                        </div>
                    `;
                    notificationsList.appendChild(notification);
                    // Add event listeners to buttons
                    document.getElementById(`acceptRequest_${friendRequest.request_id}`).addEventListener("click", (e) => {
                        e.preventDefault();
                        let requestId = e.target.getAttribute("data-request");
                        this.#manageFriendRequest(e, requestId, "accept");
                    });
                    document.getElementById(`denyRequest_${friendRequest.request_id}`).addEventListener("click", (e) => {
                        e.preventDefault();
                        let requestId = e.target.getAttribute("data-request");
                        this.#manageFriendRequest(e, requestId, "reject"); 
                    });
                }
                else if (friendRequest.request_type === "lobby_invite")
                {
                    let notification = document.createElement('a');
                    notification.classList.add('dropdown-item');
                    notification.href = '#';
                    notification.innerHTML = `
                        <div class="d-flex align-items-center" data-idrequest="${friendRequest.request_id}">
                            <div class="py-1 px-1">
                                <img class="rounded-circle" src="${friendRequest.from_user_profile_picture}" width="50" height="50" alt="Profile Picture">
                            </div>
                            <div class="flex-grow-1 px-1">
                                <div class="font-weight-bold">${friendRequest.from_user}</div>
                                <div class="text-muted small">You have a lobby invitation.</div>
                                <div class="mt-2">
                                    <button class="btn btn-success btn-sm mr-2" id="acceptInvite_${friendRequest.request_id}" data-id=${friendRequest.request_id} data-url="${friendRequest.requestUrl}">Accept</button>
                                    <button class="btn btn-danger btn-sm" id="denyInvite_${friendRequest.request_id}" data-id=${friendRequest.request_id}  data-url="${friendRequest.requestUrl}">Deny</button>
                                </div>
                            </div>
                        </div>
                    `;
                    notificationsList.appendChild(notification);
                    // Add event listeners to buttons
                    document.getElementById(`acceptInvite_${friendRequest.request_id}`).addEventListener("click", (e) => {
                        e.preventDefault();
                        let requestId = e.target.getAttribute("data-url");
                        this.#manageInvite(e, "accept", document.getElementById(`acceptInvite_${friendRequest.request_id}`));
                    });
                    document.getElementById(`denyInvite_${friendRequest.request_id}`).addEventListener("click", (e) => {
                        e.preventDefault();
                        let requestId = e.target.getAttribute("data-url");
                        this.#manageInvite(e, "reject", document.getElementById(`denyInvite_${friendRequest.request_id}`));
                    });
                }
            });
            this.#decoratorToggle();
        }
    }
    #manageInvite = (e, action, div) => {
        
        let acceptordeny = `/auth/token/invite/manage/`;
        let id = e.target.getAttribute("data-id");
        fetch(acceptordeny, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Assuming you have a getCookie function to retrieve CSRF tokens
            },
            body: JSON.stringify({
                invite_id: id,
                action: action
            })
        }).then((response) => {
            return response.json();
        }).then((data) => {
            if(action === "reject")
                return;
            this.#spaObject.setTo(data.url);
        })
    }
    
    #manageFriendRequest = (e, id, action) => {
        fetch('/auth/token/friend/request/manage/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Assuming you have a getCookie function to retrieve CSRF tokens
            },
            body: JSON.stringify({
                friend_request_id: id,
                action: action
            })
        }).then((response) => {
            return response.json();
        }).then((data) => {
        }).catch((error) => {
        });
    }



    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("headerMenu");
        this.#spaObject = spaObject;
        this.#decoratorToggle();

        let protocol = window.location.protocol === "https:" ? "wss" : "ws";
        this.#notificationSocket = new WebSocket(`${protocol}://${window.location.host}/ws/notifications/`);
        this.#notificationSocket.onmessage = (e) => {
            let data = JSON.parse(e.data);
            if (data.notifications !== undefined) {
                this.IncreaseNotificationCount("notifications", "notifications");
                if (data.Message !== undefined) {
                    this.IncreaseNotificationCount("message", "message");
                }
            }
            this.#decoratorToggle();
        };
        this.#notificationSocket.onclose = (e) => {
        };
        this.#notificationSocket.onerror = (e) => {
        };

    }

    render() {

        let url = this.getUrl();
        this._getHtml(url).then((html) => {
            let profile = document.getElementById("nav-profile");
            let friends = document.getElementById("nav-friends");
            let logout = document.getElementById("nav-logout");
            let game = document.getElementById("nav-game");
            let home = document.querySelectorAll("#nav-home");
            let notificationsDropdown = document.getElementById("notificationsDropdown");

            if(profile === null || friends === null || logout === null || game === null || home === null || notificationsDropdown === null){
                return;
            }



            home.forEach((element) => {
                element.addEventListener("click", (e) => this.navigateTo(e, "/"));
            });
            game.addEventListener("click", (e) => this.navigateTo(e, "/Game/"));
            profile.addEventListener("click", (e) => this.navigateTo(e, "/Profile/"));
            friends.addEventListener("click", (e) => this.navigateTo(e, "/Friends/"));
            logout.addEventListener("click", (e) => this.#logout(e));
            notificationsDropdown.addEventListener("click", (e) => {
                this.#numberofNotifications = 0;
                this.#decoratorToggle();

                if(document.getElementById("notificationsMenu").style.display == "block"){
                    this.#showNotifications = false;
                } else {
                    this.#showNotifications = true;
                }
                fetch('/auth/token/friend/request/get/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Assuming you have a getCookie function to retrieve CSRF tokens
                    }
                }).then((response) => {
                    return response.json();
                }).then((data) => {
                    let notificationsList = document.getElementById("notificationsMenu");
                    notificationsList.innerHTML = '';
                    this.#renderFriendRequests(data);
                }).catch((error) => {
                }
                );
            });
        });
        if(this.#deployNotifications === false){
            this.watchNotifications();
            this.#deployNotifications = true;
        }
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

    async #logout(e) {
        e.preventDefault();
        const Header = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        };
        const rep = await Requests.post('/Logout/', {}, Header);
        window.location.href = '/';
    }

    navigateTo(e, url) {
        e.preventDefault();
        this.#spaObject.setTo(url);
    }


}

export default Menu;