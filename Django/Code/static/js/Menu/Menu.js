import AComponent from "../Spa/AComponent.js";
import { Requests, getCookie } from "../Utils/Requests.js";

/*

Notification Consumer:

class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        print("WebSocket connection accepted")
        print(f"User: {user.username} and Code: {user.userSocialCode}")
        if user.is_anonymous:
            await self.close()
        else:
            # Group the user by their userSocialCode
            self.group_name = f"user_{user.userSocialCode}"
            print("Group Name: ", self.group_name)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
    async def disconnect(self, close_code):
        # Remove the user from the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    async def send_notification(self, event):
        # Send notification data to the WebSocket
        await self.send(text_data=json.dumps({
            'notifications': event['notifications']
        }))


    Object { friend_requests: (1) […] }
    friend_requests: Array [ {…} ]
        0: Object { request_id: 3, from_user: "pedro", from_user_profile_picture: "/media/Auth/defaultAssets/ProfilePicture.png", … }
    length: 1
    <prototype>: Array []
    <prototype>: Object { … }

*/

class Menu extends AComponent {
    #parentElement = null;
    #spaObject = null;
    #numberofNotifications = 0;
    #numberofMessages = 0;
    #notificationSocket = null;

    // Increase the number of notifications or messages
    Increase = (Target, event) => {
        if (event === "notification") {
            this.#numberofNotifications += 1;
        } else if (event === "message") {
            this.#numberofMessages += 1;
        }
        this.#decoratorToggle();
    }

    // Decrease the number of notifications or messages
    Decrease = (Target, event) => {
        if (event === "notification") {
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
            if (this.#doesHtmlHasClass(notificationBadge, displayOffClass)) {
                notificationBadge.classList.remove(displayOffClass);
            }
            notificationBadge.innerText = this.#numberofNotifications;
        } else {
            if (!this.#doesHtmlHasClass(notificationBadge, displayOffClass)) {
                notificationBadge.classList.add(displayOffClass);
            }
        }

        if (this.#numberofMessages > 0) {
            if (this.#doesHtmlHasClass(messagesBadge, displayOffClass)) {
                messagesBadge.classList.remove(displayOffClass);
            }
            messagesBadge.innerText = this.#numberofMessages;
        } else {
            if (!this.#doesHtmlHasClass(messagesBadge, displayOffClass)) {
                messagesBadge.classList.add(displayOffClass);
            }
        }
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
            console.log("Notification: ", data);
            if (data.notifications) {
                data.notifications.forEach((notification) => {
                    console.log("Notification: ", notification);
                    if (notification.message === "admin sent you a friend request.") {
                        this.Increase("notification", "notification");
                    } else if (notification.message === "admin sent you a message.") {
                        this.Increase("message", "message");
                    }
                });
            }
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
            // this.#parentElement.innerHTML = html;
            // let home = document.getElementById("nav-home");
            let profile = document.getElementById("nav-profile");
            let friends = document.getElementById("nav-friends");
            let logout = document.getElementById("nav-logout");
            // there are two elements with the same id to get the use all the elements with the same id
            let home = document.querySelectorAll("#nav-home");
            let notificationsDropdown = document.getElementById("notificationsDropdown");

            // home.addEventListener("click", (e) => this.navigateTo(e, "/"));
            home.forEach((element) => {
                element.addEventListener("click", (e) => this.navigateTo(e, "/"));
            });
            profile.addEventListener("click", (e) => this.navigateTo(e, "/Profile/"));
            friends.addEventListener("click", (e) => this.navigateTo(e, "/Friends/"));
            logout.addEventListener("click", (e) => this.#logout(e));
            notificationsDropdown.addEventListener("click", (e) => {
                this.#numberofNotifications = 0;
                this.#decoratorToggle();
                fetch('/get_friend_requests/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }).then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Something went wrong');
                    }
                }).then((data) => {
                    console.log(data);
                    let notificationsList = document.getElementById("notificationsMenu");
                    notificationsList.innerHTML = '';
                    if (data.friend_requests && data.friend_requests.length > 0) {
                        data.friend_requests.forEach((friendRequest) => {
                            let notification = document.createElement('a');
                            notification.classList.add('dropdown-item');
                            notification.href = '#';
                            notification.innerHTML = `
                                <div class="d-flex align-items-center" data-idrequest="${friendRequest.id}">
                                    <div class="py-1 px-1">
                                        <img class="rounded-circle" src="${friendRequest.from_user_profile_picture}" width="50" height="50" alt="Profile Picture">
                                    </div>
                                    <div class="flex-grow-1 px-1">
                                        <div class="font-weight-bold">${friendRequest.from_user}</div>
                                        <div class="text-muted small">sent you a friend request.</div>
                                        <div class="mt-2">
                                            <button class="btn btn-success btn-sm mr-2" id="acceptRequest">Accept</button>
                                            <button class="btn btn-danger btn-sm" id="denyRequest">Deny</button>
                                        </div>
                                    </div>
                                </div>
                            `;
                            notificationsList.appendChild(notification);
                            document.getElementById("acceptRequest").addEventListener("click", (e) => {
                                e.preventDefault();
                                console.log("Accept request");
                                fetch('/manage_friend_request/', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': getCookie('csrftoken')
                                    },
                                    body: JSON.stringify({
                                        friend_request_id: friendRequest.request_id,
                                        action: 'accept'
                                    })
                                }).then((response) => {
                                    if (response.ok) {
                                        return response.json();
                                    } else {
                                        throw new Error('Something went wrong');
                                    }
                                }).then((data) => {
                                    console.log(data);
                                }).catch((error) => {
                                    console.error(error);
                                });
                            });

                            document.getElementById("denyRequest").addEventListener("click", (e) => {
                                e.preventDefault();
                                console.log("Deny request");
                                fetch('/deny_friend_request/', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': getCookie('csrftoken')
                                    },
                                    body: JSON.stringify({ 
                                        friend_request_id: friendRequest.request_id,
                                        action: 'deny'
                                    })
                                }).then((response) => {
                                    if (response.ok) {
                                        return response.json();
                                    } else {
                                        throw new Error('Something went wrong');
                                    }
                                }).then((data) => {
                                    console.log(data);
                                }).catch((error) => {
                                    console.error(error);
                                });
                            });
                        });
                    }
                }).catch((error) => {
                    console.error(error);
                });
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
        // window.location.href = '/';
    }

    navigateTo(e, url) {
        e.preventDefault();
        console.log("Navigate to: ", url);
        console.log("SPA Object: ", this.#spaObject);
        this.#spaObject.setTo(url);
    }
}

export default Menu;