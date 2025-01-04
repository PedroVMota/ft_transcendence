import AComponent from "../Spa/AComponent.js";

export default class Lobby extends AComponent {
    #webSocket = null
    #parentElement = null
    #lobbyId = ''

    constructor(url, spaObject, lobbyID)
    {
        super(url, spaObject);
        let protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        let host = window.location.host;
        let path = "/ws/Monitor/Lobby/" + lobbyID + "/";
        
        this.#webSocket = new WebSocket(`${protocol}://${host}${path}`);
        this.#parentElement = document.getElementById("root");
        this.#lobbyId = lobbyID;
    }

    render()
    {
        console.log("Rendering Lobby");

        if (this.#parentElement.innerHTML !== ''){
            this.#setWebSocketEventHandlers();
            this.#setEventHandlers();
            console.log("Parent element not empty");
            return;
        }

        const url = this.getUrl();

        this._getHtml(url)
            .then((html) => {
                const newDom = new DOMParser().parseFromString(html, 'text/html');
                document.head.innerHTML = newDom.head.innerHTML;
                const root = newDom.getElementById("root");
                if (!root)
                {
                    console.log("Root element not found in fetched HTML");
                    this.#setWebSocketEventHandlers();
                    this.#setEventHandlers();
                    console.error("Root not found in fetched HTML");
                    return;
                }

                this.#parentElement.innerHTML = root.innerHTML;
                this.#setWebSocketEventHandlers();
                this.#setEventHandlers();

            })
            .catch((error) => {
                console.error("Error fetching HTML: ", error);
            })
        
    }

    #setWebSocketEventHandlers() {
        console.log("Setting WebSocket event handlers");
        this.#webSocket.onopen = function () {
            console.log('WebSocket connection established');
        };
    
        this.#webSocket.onmessage = function (event) {
            console.log(`Message arrived: ${event.data}`);
            const data = JSON.parse(event.data);
            const messagesDiv = document.getElementById('messages');
            const newMessage = document.createElement('p');
            newMessage.innerHTML = `<strong>Server:</strong> ${data.message}`;
            if (data['action'] === 'lobby-message-submission') {
                newMessage.innerHTML = data['message'];
                console.log("Message arrived from WebSocket");
            }
            messagesDiv.appendChild(newMessage);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        };
    
        this.#webSocket.onerror = function (error) {
            console.error("WebSocket error: ", error);
        };
    
        this.#webSocket.onclose = function () {
            console.log('WebSocket connection closed');
        };
    }


    #setEventHandlers()
    {
        document.getElementById('chatForm').addEventListener('submit', function (event) {
        event.preventDefault();
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value;
        console.log(message);
        ws.send(JSON.stringify({
            'action': 'message-sent-on-lobby',
            'lobby': lobbyId,
            'message': message
        }));
        messageInput.value = '';
        });

        const overlays = document.querySelectorAll('.overlay');
        console.log(overlays);
        overlays.forEach(overlay => {
            overlay.addEventListener('click', function() {
                console.log(overlay.dataset.userCode);
                spa.setTo('/Profile/' + overlay.dataset.userCode + "/");
            });
        });

        window.addEventListener('popstate', (event) => {
            spa.loadPage();
        });
    }

}