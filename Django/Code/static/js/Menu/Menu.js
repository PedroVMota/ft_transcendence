import AComponent from "../Spa/AComponent.js";
import { Requests, getCookie } from "../Utils/Requests.js";


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

    // Increase the number of notifications or messages
    Increase = (Target, event) => {
        console.log("Increase: ", event);
        if (event === "notifications") {
            this.#numberofNotifications += 1;
        } else if (event === "message") {
            this.#numberofMessages += 1;
        }
        event === "m"
        this.#decoratorToggle();
    }

    // Decrease the number of notifications or messages
    Decrease = (Target, event) => {
        if (event === "notifications") {
            this.#numberofNotifications -= 1;
        } else if (event === "message") {
            this.#numberofMessages -= 1;
        }
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
        let displayOffClass = "d-none";

        if (this.#numberofNotifications > 0) {
            if (this.#doesHtmlHasClass(notificationBadge, displayOffClass))
                notificationBadge.classList.remove(displayOffClass);
            notificationBadge.innerText = this.#numberofNotifications;
        }
        else {
            if (!this.#doesHtmlHasClass(notificationBadge, displayOffClass))
                notificationBadge.classList.add(displayOffClass);
        }

        if (this.#numberofMessages > 0) {
            if (this.#doesHtmlHasClass(messagesBadge, displayOffClass))
                messagesBadge.classList.remove(displayOffClass);
            messagesBadge.innerText = this.#numberofMessages;
        }
        else {
            if (!this.#doesHtmlHasClass(messagesBadge, displayOffClass))
                messagesBadge.classList.add(displayOffClass);
        }
    }

    #renderFriendRequests = (data) => {
        let notificationsList = document.getElementById("notificationsMenu");
        let notificationBadge = document.getElementById("notificationBadge");

        if (data.friend_requests === undefined || data.friend_requests.length === 0) {

            notificationsList.innerHTML = `<li><span class="dropdown-item-text">No new notifications</span></li>`;
            notificationBadge.textContent = '0';

        } else {
            notificationBadge.textContent = data.friend_requests.length;
            data.friend_requests.forEach((friendRequest) => {
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
                            <button class="btn btn-success btn-sm mr-2" id="acceptRequest_${friendRequest.request_id}">Accept</button>
                            <button class="btn btn-danger btn-sm" id="denyRequest_${friendRequest.request_id}">Deny</button>
                        </div>
                    </div>
                </div>
                `;
                notificationsList.appendChild(notification);
                document.getElementById(`acceptRequest_${friendRequest.request_id}`).addEventListener("click", (e) => {
                    e.preventDefault();
                    console.log("Accept request");
                    Requests.post('/manage_friend_request/', {
                        friend_request_id: friendRequest.request_id,  // Changed to request_id
                        action: 'accept'
                    }, this.#defaultHeader).then((data) => {
                        console.log(data);
                    }).catch((error) => {
                        console.error(error);
                    });
                });
                document.getElementById(`denyRequest_${friendRequest.request_id}`).addEventListener("click", (e) => {
                    e.preventDefault();
                    console.log("Deny request");
                    Requests.post('/deny_friend_request/', {
                        friend_request_id: friendRequest.request_id,  // Changed to friendRequest.request_id
                        action: 'deny'
                    }, this.#defaultHeader).then((data) => {
                        console.log(data);
                    }).catch((error) => {
                        console.error(error);
                    });
                });


            });
        }

        this.#decoratorToggle();
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
            console.log("WebSocket message: ", data);
            if (data.notifications !== undefined) {
                this.Increase("notifications", "notifications");
                if (data.Message !== undefined) {
                    this.Increase("message", "message");
                }
            }
            this.#decoratorToggle();
        };
        this.#notificationSocket.onclose = (e) => {
            console.log("WebSocket closed: ", e);
        };
        this.#notificationSocket.onerror = (e) => {
            console.log("WebSocket error: ", e);
        };

    }

    render() {
        let url = this.getUrl();
        this._getHtml(url).then((html) => {
            let profile = document.getElementById("nav-profile");
            let friends = document.getElementById("nav-friends");
            let logout = document.getElementById("nav-logout");
            let home = document.querySelectorAll("#nav-home");
            let notificationsDropdown = document.getElementById("notificationsDropdown");

            home.forEach((element) => {
                element.addEventListener("click", (e) => this.navigateTo(e, "/"));
            });
            profile.addEventListener("click", (e) => this.navigateTo(e, "/Profile/"));
            friends.addEventListener("click", (e) => this.navigateTo(e, "/Friends/"));
            logout.addEventListener("click", (e) => this.#logout(e));
            notificationsDropdown.addEventListener("click", (e) => {
                this.#numberofNotifications = 0;
                this.#decoratorToggle();
                Requests.get('/get_friend_requests/', this.#defaultHeader).then((data) => {
                    console.log(data);
                    let notificationsList = document.getElementById("notificationsMenu");
                    notificationsList.innerHTML = '';
        
                    this.#renderFriendRequests(data);
                }).catch((error) => {
                    console.error(error);
                }
                );
            });
        });
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
        console.log(rep);
        window.location.href = '/';
    }

    navigateTo(e, url) {
        e.preventDefault();
        console.log("Navigate to: ", url);
        console.log("SPA Object: ", this.#spaObject);
        this.#spaObject.setTo(url);
    }


}

export default Menu;