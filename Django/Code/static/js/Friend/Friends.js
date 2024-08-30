import AComponent from "../Spa/AComponent.js";
import { Requests } from "../Utils/Requests.js";
import AWebChat from "../Utils/ASocket.js";

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

class WebSocketClient extends AWebChat {
    constructor(url) {
        super(url);
        this.connect();
    }

    connect() {
        this._ws.onopen = this.onOpen.bind(this);
        this._ws.onmessage = this.onMessage.bind(this);
        this._ws.onclose = this.onClose.bind(this);
        this._ws.onerror = this.onError.bind(this);
    }

    sendMessage(data) {
        this._ws.send(data);
    }

    onMessage(event) {
        console.log('WebSocket message received:', event.data);
        this.#addMessageToChat(event.data);
    }

    onOpen() {
        console.log('WebSocket connection opened');
    }

    onClose() {
        console.log('WebSocket connection closed');
    }

    onError(error) {
        console.error('WebSocket error:', error);
    }

    #addMessageToChat(data) {
        const chatMessages = document.querySelector('.chat-messages');
        const messageData = JSON.parse(data);
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message');
        messageElement.innerHTML = `<strong>${messageData.username}:</strong> ${messageData.message}`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    bindSendButton() {
        document.getElementById('sendMenssage').addEventListener('click', () => {
            console.log('Button clicked');
            const input = document.getElementById('inputVal');
            const message = input.value;
            if (message) {
                const username = 'You'; // Replace with dynamic username if needed
                const data = JSON.stringify({ username, message });
                this._ws.send(data);
                input.value = '';
            }
        });
    }
}

export default class Friends extends AComponent {
    #parentElement = null;
    #spaObject = null;
    #socket = null;

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const hostname = window.location.hostname;
        const port = window.location.port ? `:${window.location.port}` : '';
        const wsUrl = `${protocol}//${hostname}${port}/ws/general/`;
        this.#socket = new WebSocketClient(wsUrl);
    }

    render() {
        let url = this.getUrl();
        this.#parentElement.innerHTML = '<span>Pending...</span>';

        this._getHtml(url).then((html) => {
            let documentResponse = new DOMParser().parseFromString(html, 'text/html');
            let rootContentHtml = documentResponse.getElementById('root').innerHTML;
            if (rootContentHtml) {
                document.head.innerHTML = documentResponse.head.innerHTML;
                this.#parentElement.innerHTML = rootContentHtml;

                // Initialize search user events
                this.#renderOnChange();

                setTimeout(() => {
                    this.hideSpinner();
                }, 1000);

                this.#socket.bindSendButton();
            }
        }).catch((error) => {
            console.error(error);
        });

    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

    
    #renderOnChange() {
        const searchInput = document.querySelector('.form-control[placeholder="Search or add a friend..."]');
        const searchButton = document.querySelector('.btn[type="button"]');
        const searchResultsList = document.getElementById('search-results-list');
        console.log(searchInput, searchButton, searchResultsList);

        if (searchButton && searchInput) {
            searchInput.addEventListener('input', () => {
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
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Search results:', data);
                        if (data.friends && data.friends.length > 0) {
                            data.friends.forEach(friend => {
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

                                searchResultsList.appendChild(friendItem);

                                friendItem.querySelector('.add-friend-btn').addEventListener('click', function(e) {
                                    e.preventDefault();
                                    const userCode = searchInput.value.trim();
                                    console.log('Sending friend request to:', userCode);
                                    fetch('/send_friend_request/', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'X-CSRFToken': getCookie('csrftoken')
                                        },
                                        body: JSON.stringify({ user_code: userCode })
                                    }).then(response => {
                                        console.log('Friend request sent:', response);
                                        return response.json();
                                    }).then(data => {
                                        alert(data.message);
                                    }).catch(error => {
                                        console.error('Error sending friend request:', error);
                                    });
                                });
                            });
                        } else if (data.error) {
                            const errorItem = document.createElement('div');
                            errorItem.className = 'text-danger';
                            errorItem.textContent = data.error;
                            searchResultsList.appendChild(errorItem);
                        }
                    })
                    .catch(error => {
                        console.error('Error during search:', error);
                        alert('An error occurred while searching. Please try again.');
                    });
            });
        } else {
            console.error('Search input or button not found');
        }
    }
}
