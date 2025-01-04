import AComponent from "../Spa/AComponent.js";
import spa from "../Spa/Spa.js";

export default class Friends extends AComponent {
    #parentElement = null;
    #spaObject = null;
    #socket = null;
    #activeChatId = null;
    #userSocialCode = null;

    constructor(url, spaObject) {
        super(url, spaObject)
        this.#parentElement = document.getElementById("root")
        this.#spaObject = spaObject;
    }

    render() {
        const url = this.getUrl()
        this._getHtml(url).then((html) => {
            let doomResponse = new DOMParser().parseFromString(html, 'text/html');
            let rootContentHtml = doomResponse.getElementById('root').innerHTML;
            if (rootContentHtml) {
                document.head.innerHTML = doomResponse.head.innerHTML;
                this.#parentElement.innerHTML = rootContentHtml;
                this.#initializeEventListeners();
                this.#visualizeProfile();
            }
            else {
                null
            }
        }).catch((error) => {
            console.error('Error fetching HTML:', error);
        });
    }

    destroy() {
        this.#parentElement.innerHTML = ''
        if (this.#socket) this.#socket.close();
    }

    #initializeEventListeners() {
        const chatItems = document.querySelectorAll('#toggle_Chat');
        chatItems.forEach(item => {
            item.addEventListener('click', () => this.#handleChatItemClick(item));
        });
        const inputField = document.querySelector('.chat-input-section input');
        inputField.addEventListener('keypress', (event) => this.#handleMessageSend(event));

        // Initialize search event listener
        this.#initializeSearch();
    }

    #handleChatItemClick(item) {
        const conversationId = item.getAttribute('data-conversationId')
        const userFirstLast = item.querySelector('.text-white').innerText
        const userCode = item.getAttribute('data-usercode')
        let doom = new DOMParser().parseFromString(item.outerHTML, 'text/html');
        let profile_picture = doom.getElementById('target_profile').getAttribute('src');

        let user_profile_picture = document.getElementById('user_profile_picture');
        let user_first_last = document.getElementById('user_first_last');
        let user_code = document.getElementById('user_code');

        if (this.#activeChatId === conversationId) {
            return;
        }
        this.#activeChatId = conversationId;
        console.log(item);
        this.#markChatAsActive(item);
        if (user_profile_picture) {
            user_profile_picture.setAttribute('src', profile_picture);
        }
        if (user_first_last) {
            user_first_last.innerText = userFirstLast;
        }
        if (user_code) {
            user_code.innerText = userCode;
        }
        doom.close();
        this.#showChatComponents();
        this.#clearChat();
        this.#connectWebSocket(conversationId);
    }

    #markChatAsActive(item) {
        const chatItems = document.querySelectorAll('#toggle_Chat');
        chatItems.forEach(i => i.classList.remove('active'))
        item.classList.add('active');
    }

    #clearChat() {
    
        const chatWidget = document.querySelector('.chat-widget');
        if(!chatWidget) return;
        chatWidget.innerHTML = '';
    }

    #connectWebSocket(conversationId) {
        let protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        let url = `${protocol}://${window.location.host}/ws/privchat/${conversationId}/`;

        
        if (this.#socket) this.#socket.close();

        this.#socket = new WebSocket(url);

        this.#socket.onmessage = (event) => this.#handleSocketMessage(event);
        this.#socket.onerror = (e) => this.#handleSocketError(e);
        this.#socket.onopen = (e) => this.#handleSocketOpen(e);
    }

    #handleSocketOpen(e) {
    }

    #handleSocketError(e) {
        console.error("WebSocket error:", e);
    }

    #handleSocketMessage(event) {
        const data = JSON.parse(event.data);
        const chatWidget = document.querySelector('.chat-widget');
        if(!chatWidget) return;

        if (data.type === 'user_data') {
            this.#userSocialCode = data.userSocialCode;
            return;
        }

        const messageElement = this.#createMessageElement(data);
        chatWidget.appendChild(messageElement);

        this.#scrollToBottom(chatWidget);
    }

    #scrollToBottom(chatWidget) {
        chatWidget.scrollTop = chatWidget.scrollHeight;
    }

    #createMessageElement(data) {
        const messageClass = data.userSocialCode === this.#userSocialCode ? 'message-mine' : 'message-other';
        const alignmentClass = data.userSocialCode === this.#userSocialCode ? 'text-end' : 'text-start';
        const messageColorClass = data.userSocialCode === this.#userSocialCode ? 'mine-bg text-white' : 'bg-secondary text-white';

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', messageClass, 'd-flex', 'mb-3');
        messageElement.innerHTML = `
            <div class="message-content bg-transparent p-1 border-1 ${alignmentClass}">
                <span class="text-white fs-6">${data.userSocialCode === this.#userSocialCode ? 'You' : data.user}</span>
                <div class="message-text ${messageColorClass} p-2 rounded">
                    ${data.message}
                </div>
            </div>
        `;
        return messageElement;
    }

    #showChatComponents() {
        const waitingDiv = document.getElementById('Wating');
        const chatTop = document.getElementById('chat_top');
        const chatBody = document.getElementById('chat_body');
        const chatInput = document.getElementById('chat_input');

        if(!waitingDiv || !chatTop || !chatBody || !chatInput) return;


        waitingDiv.style.cssText = 'display: none !important';
        chatTop.style.cssText = 'display: flex !important';   
        chatBody.style.cssText = 'display: flex !important';  
        chatInput.style.cssText = 'display: block !important';
    }

    #handleMessageSend(event) {
        const inputField = event.target;


        if (event.key === 'Enter' && this.#socket && this.#socket.readyState === WebSocket.OPEN) {
            const message = inputField.value.trim();
            if (message) {
                this.#socket.send(JSON.stringify({
                    'message': message
                }));

                inputField.value = '';

                const chatWidget = document.querySelector('.chat-widget');
                this.#scrollToBottom(chatWidget);
            }
        }
    }

    // New methods for handling search functionality

    #initializeSearch() {
        const form = document.querySelector('.search-bar form');
        const searchResults = document.getElementById('search-results');

        if (!form || !searchResults) return;

        if (form) {
            form.addEventListener('submit', (e) => this.#handleSearchSubmit(e, form, searchResults));
        }
    }

    #handleSearchSubmit(e, form, searchResults) {
        e.preventDefault();
        if (!searchResults) return;
        const searchField = form.querySelector('#searchField');
        if(!searchField) return;
        const searchValue = searchField.value.trim();
        const isInt = /^\d+$/.test(searchValue);
        let data = {};

        // Prepare data depending on whether it's a username or user_code search
        if (isInt) {
            data = { user_code: searchValue };
        } else {
            data = { username: searchValue };
        }

        // Send search request
        this.#performSearch(form, data, searchResults);
    }

    async #performSearch(form, data, searchResults) {
        try {
            const response = await fetch("/searchUser/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if (result && result.user && result.user.Info) {
                this.#renderSearchResults(result.user, searchResults);
            }
        } catch (error) {
            console.error('Error during search:', error);
        }
    }

    #renderSearchResults(user, searchResults) {
        const searchResultsList = document.getElementById('search-results-list');
        if(!searchResultsList) return;
        if (searchResultsList) {

            searchResultsList.innerHTML = '';
            const userItem = document.createElement('a');
            userItem.classList.add('list-group-item', 'border-0', 'list-group-item-action', 'bg-transparent', 'd-flex', 'justify-content-between', 'align-items-center');
            userItem.href = `javascript:void(0)`;  // Use javascript:void(0) to prevent full page reload
            userItem.setAttribute('data-profile', user.Info.userCode); // Attach user code
            
            userItem.innerHTML = `
                <div class="d-flex align-items-center text-white">
                    <img src="${user.Info.profile_picture}" style="width: 50px; height: 50px;">
                    <div class="ms-3 text-white">
                        <h5 class="mb-0">${user.Info.first_name} ${user.Info.last_name}</h5>
                        <small class="text-muted fs-6 text-white-50">${user.Info.userCode}</small>
                    </div>
                </div>
                <span data-role="profile-entrypoint" data-profile="${user.Info.userCode}" class="btn btn-sm"><i class="fas fa-eye text-white"></i></span>
            `;
            searchResultsList.appendChild(userItem);
            let goto_Profile = document.querySelectorAll('[data-role="profile-entrypoint"]');
            for (let i = 0; i < goto_Profile.length; i++) {
                goto_Profile[i].addEventListener('click', (e) => {
                    e.preventDefault();
                    let userCode = goto_Profile[i].getAttribute('data-profile');
                    if (this.#socket !== null)
                        this.#socket.close();
                    spa.setTo(`/Profile/${userCode}/`);
                });
            }
    
            setTimeout(() => {
                userItem.classList.add('show');
            }, 10);
        }
    }

    #visualizeProfile(){
        let goto_Profile = document.querySelectorAll("#goto_Profile");

        for (let i = 0; i < goto_Profile.length; i++) {
            goto_Profile[i].addEventListener('click', (e) => {
                e.preventDefault();
                let userCode = goto_Profile[i].getAttribute('data-profile');
                if (this.#socket !== null)
                    this.#socket.close();
                spa.setTo(`/Profile/${userCode}/`);
        });
        }
    }
}
