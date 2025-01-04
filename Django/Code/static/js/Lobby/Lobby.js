import AComponent from "../Spa/AComponent.js";
import spa from "../Spa/Spa.js";

export default class Lobby extends AComponent {
    #webSocket = null
    #parentElement = null
    #lobbyId = ''

    constructor(url, spaObject, lobbyID)
    {
        super(url, spaObject);
        this.#webSocket = new WebSocket("ws://" + window.location.host + "/ws/Monitor/Lobby/" + lobbyID + "/");
        this.#parentElement = document.getElementById("root");
        this.#lobbyId = lobbyID;
    }

    render()
    {
        console.log("Rendering Lobby");

        if (this.#parentElement.innerHTML !== ''){
            console.log("Parent element not empty");
            return;
        }

        const url = this.getUrl();

        this._getHtml(url)
            .then((html) => {
                const newDom = new DOMParser().parseFromString(html, 'text/html');

                const root = newDom.getElementById("root");
                if (!root)
                {
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

    #setWebSocketEventHandlers()
    {
        this.#webSocket.onmessage = function ()
        {
            console.log('WebSocket connection established');
        };

        this.#webSocket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            const messagesDiv = document.getElementById('messages');
            const newMessage = document.createElement('p');
            newMessage.innerHTML = `<strong>Server:</strong> ${data.message}`;
            if (data['action'] === 'lobby-message-submission')
            {
                newMessage.innerHTML = data['message'];
            console.log("message arrived from web socket")
            messagesDiv.appendChild(newMessage);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        console.log('something');
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