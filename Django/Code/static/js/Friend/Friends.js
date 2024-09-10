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

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
    }

    #getChat() {
        let listGroup = document.getElementById('friends-list');

        Requests.get('/get_chat_user/', {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }).then((response) => {
            let chats = response.chats;
            if (chats.length > 0) {
                listGroup.innerHTML = ''; // Clear existing content
                chats.forEach((chat) => {
                    let friendItem = document.createElement('a');
                    friendItem.href = 'javascript:void(0);';
                    friendItem.className = 'list-group-item list-group-item-action d-flex friend-item acrylicStyle';
                    friendItem.id = chat.unique_id;
                    friendItem.dataset.id = chat.unique_id;
                    friendItem.innerHTML = `
                        <div class="position-relative">
                            <img src="${chat.profile_picture}" alt="${chat.username}">
                            <span class="friend-status status-online position-absolute"></span>
                        </div>
                        <div class="friend-info">
                            <div>${chat.username}</div>
                        </div>
                    `;
                    listGroup.appendChild(friendItem);

                    // Check if the chat is already active, don't reconnect if so
                    friendItem.addEventListener('click', () => {
                        if (this.#activeChatId !== chat.unique_id) {
                            this.#connectToChat(chat.unique_id);
                        } else {
                            console.log('Chat is already active.');
                        }
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
        this.#socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.#displayMessage(data.message, data.user, data.create_date);
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

    #displayMessage(message, user, createDate) {
        const chatMessages = document.getElementById('target_chat');
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.innerHTML = `<strong>${user} (${createDate}):</strong> ${message}`;
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
        friendItem.className = 'list-group-item list-group-item-action d-flex friend-item acrylicStyle';
        friendItem.innerHTML = `
            <div class="position-relative">
                <img src="${friend.profile_picture}" alt="${friend.username}">
                <span class="friend-status status-online position-absolute"></span>
            </div>
            <div class="friend-info">
                <div>${friend.username}</div>
                <div class="text-muted small">${friend.email}</div>
            </div>
            <button class="btn btn-primary add-friend-btn" data-username="${friend.username}">Add Friend</button>
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
