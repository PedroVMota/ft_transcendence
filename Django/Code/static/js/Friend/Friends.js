import AComponent from "../Spa/AComponent.js";
import { Requests } from "../Utils/Requests.js";
import WebSocketClient from "./NotificationSocket.js";

// Helper function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export default class Friends extends AComponent {
    #parentElement = null;
    #spaObject = null;
    #socket = null;
    #activeChatId = null;  // Track the active chat
    #selectedFriendItem = null; 

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
        this.mySocialCode = 0;  // Set the user's social code
    }

    #getChat() {
        let listGroup = document.getElementById('friends-list');

        Requests.get('/get_chat_user/', {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrftoken
        }).then((response) => {
            let chats = response.chats;
            if (chats.length > 0) {
                listGroup.innerHTML = ''; // Clear existing content
                chats.forEach((chat) => {
                    let friendItem = document.createElement('a');
                    friendItem.href = 'javascript:void(0);';
                    friendItem.className = 'list-group-item list-group-item-action p-0 my-1 friend-item acrylicStyle';
                    friendItem.id = chat.unique_id;
                    friendItem.dataset.id = chat.unique_id;
                    friendItem.innerHTML = `
                        <div class="friend-info">
                            <img src="${chat.profile_picture}" class="rounded-circle m-3 friend-control profile-photo">
                            <span>${chat.username}</span>
                        </div>
                        <div class="friend-controls d-flex flex-column acrylicStyle p-1">
                            <button class="btn block-friend icon-centered" id="remove_${chat.unique_id}">
                                <img src="/static/svg/userDelete.svg" width="25" height="25" >
                            </button>
                            <button class="btn remove-friend icon-centered" id="block_${chat.unique_id}">
                                <img src="/static/svg/userBlock.svg" width="25">
                            </button>
                        </div>
                    `;
                    listGroup.appendChild(friendItem);

                    friendItem.addEventListener('click', () => {
                        // Check if the chat is already active
                        if (this.#activeChatId !== chat.unique_id) {
                            this.#connectToChat(chat.unique_id);
                        
                            // Update the "selected" class for the clicked friend item
                            if (this.selectedFriendItem) {
                                // Remove the "selected" class from the previously selected friend item
                                this.selectedFriendItem.classList.remove('selected');
                            }
                        
                            // Add the "selected" class to the currently clicked friend item
                            friendItem.classList.add('selected');
                        
                            // Update the reference to the currently selected friend item
                            this.selectedFriendItem = friendItem;
                        } else {
                            console.log('Chat is already active.');
                        }
                    });
        

                    // Block user button event listener
                    const blockButton = document.getElementById(`block_${chat.unique_id}`);
                    blockButton.addEventListener('click', (e) => {
                        e.stopPropagation();  // Prevent triggering the chat open event
                        console.log(`user_${chat.unique_id} blocked`);

                        // AJAX request to block the user
                        fetch(`/manage/block/${chat.unique_id}/`, {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': this.csrftoken,  // Use CSRF token
                                'Content-Type': 'application/json'
                            }
                        }).then(response => response.json())
                            .then(data => console.log(data.message))
                            .catch(error => console.error('Error blocking user:', error));
                    });

                    // Remove friend button event listener
                    const removeButton = document.getElementById(`remove_${chat.unique_id}`);
                    removeButton.addEventListener('click', (e) => {
                        e.stopPropagation();  // Prevent triggering the chat open event
                        console.log(`user_${chat.unique_id} removed`);

                        // AJAX request to remove the friend
                        fetch(`/manage/remove/${chat.unique_id}/`, {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': this.csrftoken,  // Use CSRF token
                                'Content-Type': 'application/json'
                            }
                        }).then(response => response.json())
                            .then(data => console.log(data.message))
                            .catch(error => console.error('Error removing user:', error));
                    });
                });
            } else {
                listGroup.innerHTML = '<p>No chats available.</p>';
            }
        }).catch((error) => {
            console.error('Error fetching chat data:', error);
            listGroup.innerHTML = '<p>Error fetching chat data.</p>';
        });
    }

    #connectToChat(chatId) {
        // If the chat is already active, don't reconnect
        if (this.#activeChatId === chatId) {
            console.log('Chat is already active, not reconnecting.');
            return;
        }

        // Close the previous socket if there was one
        if (this.#socket) {
            this.#socket.close();
        }

        // Create a new WebSocket connection
        this.#socket = new WebSocket(`wss://${window.location.host}/ws/privchat/${chatId}/`);

        // Mark the chat as active
        this.#activeChatId = chatId;

        // Open WebSocket connection
        this.#socket.onopen = () => {
            console.log('WebSocket connection established');
            document.getElementById('target_chat').dataset.uuid = chatId;
        };

        // Handle incoming messages (both previous and new ones)
        // WebSocket connection
        this.#socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            // Check if it's the initial user data message
            if (data.type === 'user_data') {
                this.mySocialCode = data.userSocialCode;  // Store the user's social code
                console.log(`My social code is: ${this.mySocialCode}`);
                return;  // Exit early since this is just the user data
            }

            // For normal chat messages
            const isMe = data.userSocialCode === this.mySocialCode;  // Compare the social code
            this.#displayMessage(data.message, data.user, data.create_date, isMe, data.profile_picture);
        };


        // Handle WebSocket close event
        this.#socket.onclose = (event) => {
            console.log('WebSocket connection closed', event);
            // If the connection is closed, reset the active chat ID
            this.#activeChatId = null;
        };

        // Handle WebSocket errors
        this.#socket.onerror = (error) => {
            console.error('WebSocket error', error);
        };

        // Send a message when the form is submitted
        const sendMessageForm = document.getElementById('sendMenssage');
        sendMessageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const inputVal = document.getElementById('inputVal').value;
            if (inputVal) {
                this.#socket.send(JSON.stringify({
                    'message': inputVal
                }));
                document.getElementById('inputVal').value = '';
            }
        });
    }

    #displayMessage(message, user, createDate, isMe, profile_picture) {
        const chatMessages = document.getElementById('target_chat');

        const messageElement = document.createElement('div');
        messageElement.className = 'd-flex';
        if (isMe) {
            // Align message from "me" to the right
            console.log(profile_picture);
            messageElement.className += ' d-flex justify-content-end';  // Add 'd-flex' for proper flexbox layout
            messageElement.innerHTML = `
                <div class="message-content  text-white p-2 rounded ml-2">
                    <span class="font-weight-bold"><b>Me</b></span>
                    <div class="message-text">${message}</div>
                </div>
                <div class="profile-photo">
                     <img src="${profile_picture.includes('/media/') ? profile_picture : '/media/' + profile_picture}" class="mr-1 rounded-circle profile-photo" />
                </div>
            `;
        } else {
            // Align message from other users to the left
            console.log(profile_picture);
            messageElement.className += ' d-flex justify-content-start';  // Add 'd-flex' for proper flexbox layout
            messageElement.innerHTML = `
                <div class="profile-photo">
                    <img src="${profile_picture.includes('/media/') ? profile_picture : '/media/' + profile_picture}" class="mr-1 rounded-circle profile-photo" />
                </div>
                <div class="message-content text-white p-2 rounded ml-2">
                    <span class="font-weight-bold"><b>${user}</b></span>
                    <div class="message-text">${message}</div>
                </div>
            `;
        }

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the latest message
    }

    render() {
        const url = this.getUrl();
        this.#parentElement.innerHTML = '<span>Loading...</span>';

        this._getHtml(url).then((html) => {
            const documentResponse = new DOMParser().parseFromString(html, 'text/html');
            const rootContentHtml = documentResponse.getElementById('root').innerHTML;
            if (rootContentHtml) {
                document.head.innerHTML = documentResponse.head.innerHTML;
                this.#parentElement.innerHTML = rootContentHtml;

                // Initialize search user events
                this.#initializeSearchEvents();
                this.#getChat();
            }
        }).catch((error) => {
            console.error('Error fetching HTML:', error);
        });
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

    #initializeSearchEvents() {
        const searchInput = document.querySelector('.form-control[placeholder="Search or add a friend..."]');
        const searchResultsList = document.getElementById('search-results-list');

        if (searchInput) {
            searchInput.addEventListener('input', () => this.#handleSearchInput(searchInput, searchResultsList));
        } else {
            console.error('Search input not found');
        }
    }

    #handleSearchInput(searchInput, searchResultsList) {
        const userCode = searchInput.value.trim();
        if (userCode === "") {
            return;
        }
        searchResultsList.innerHTML = '';
        const searchQuery = `/searchUser?user_code=${encodeURIComponent(userCode)}`;
        fetch(searchQuery, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => response.json())
            .then(data => this.#renderSearchResults(data, searchResultsList, searchInput))
            .catch(error => {
                console.error('Error during search:', error);
                alert('An error occurred while searching. Please try again.');
            });
    }

    #renderSearchResults(data, searchResultsList, searchInput) {
        if (data.friends && data.friends.length > 0) {
            data.friends.forEach(friend => {
                const friendItem = this.#createFriendItem(friend);
                searchResultsList.appendChild(friendItem);

                friendItem.querySelector('.add-friend-btn').addEventListener('click', (e) => {
                    e.preventDefault();
                    this.#sendFriendRequest(searchInput.value.trim());
                });
            });
        } else if (data.error) {
            const errorItem = document.createElement('div');
            errorItem.className = 'text-danger';
            errorItem.textContent = data.error;
            searchResultsList.appendChild(errorItem);
        }
    }

    #createFriendItem(friend) {
        const friendItem = document.createElement('a');
        friendItem.href = '#';
        // friendItem.className = 'list-group-item list-group-item-action d-flex friend-item acrylicStyle';
        friendItem.className = 'list-group-item list-group-item-action p-0 friend-item acrylicStyle'
        friendItem.innerHTML = `
            <div class="friend-info">
                <img src="${friend.profile_picture}" alt="${friend.username}" class="rounded-circle m-2 profile-photo">
                <div class="d-flex flex-column">
                    <div class="friend-username font-weight-bold">${friend.username}</div>
                </div>
            </div>
            <div class="friend-controls p-1 pointer"  style="align-content: center;">
                <button class="btn add-friend-btn" data-username="${friend.username}">
                    <img src="/static/svg/userAdd.svg" width="25"/>
                </button>
            </div>
        `;

        return friendItem;
    }

    #sendFriendRequest(userCode) {
        fetch('/send_friend_request/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ user_code: userCode })
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error('Error sending friend request:', error);
            });
    }
}
