import AComponent from "../Spa/AComponent.js";

export default class Lobby extends AComponent {
    #webSocket = null
    #parentElement = null
    #lobbyId = ''
    #spa = null

    constructor(url, spaObject, lobbyID)
    {
        super(url, spaObject);
        let protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        let host = window.location.host;
        let path = "/ws/Monitor/Lobby/" + lobbyID + "/";
        
        this.#webSocket = new WebSocket(`${protocol}://${host}${path}`);
        this.#parentElement = document.getElementById("root");
        this.#lobbyId = lobbyID;
        this.#spa = spaObject;
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


            let jsonMsg = JSON.parse(event.data);

            if (jsonMsg['action'] === 'lobby-message-submission')
            {
                let msgDiv = document.getElementById('messages');
                let newMsg = document.createElement('p');
                newMsg.innerHTML = `<strong>${jsonMsg['user']}</strong> ${jsonMsg['message']}`;
                msgDiv.appendChild(newMsg);

                msgDiv.appendChild(newMsg);
                msgDiv.scrollTop = msgDiv.scrollHeight;
            }

            console.log(jsonMsg);
            let type = jsonMsg['type'];
            if(type === 'notification')
            {
                let msgDiv = document.getElementById('messages');
                let newMsg = document.createElement('p');
                newMsg.innerHTML = `<strong>Notification:</strong> ${jsonMsg['message']}`;
                msgDiv.appendChild(newMsg);
                msgDiv.appendChild(newMsg);
                msgDiv.scrollTop = msgDiv.scrollHeight;
                
            }
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
        document.getElementById('chatForm').addEventListener('submit', (event) => {
            event.preventDefault();
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value;
            console.log(message);
            this.#webSocket.send(JSON.stringify({
                'action': 'message-sent-on-lobby',
                'lobby': this.#lobbyId,
                'message': message
            }));
            messageInput.value = '';
        })

        const overlays = document.querySelectorAll('.overlay');
        console.log(overlays);
        overlays.forEach(overlay => {
            overlay.addEventListener('click', () => {
                console.log(overlay.dataset.userCode);
                this.#spa.setTo('/Profile/' + overlay.dataset.userCode + "/");
            });
        });

        window.addEventListener('popstate', (event) => {
            this.#spa.loadPage();
        });

        document.getElementById("start-game-button").addEventListener('click', (event) => {
            event.preventDefault();
            const url = 'api/game/get/';
            const data = {
                'uuid': this.#lobbyId,
            };
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(data)
            }).then(response => {
                if (!response.ok)
                {
                    throw new Error('Network response was not ok');
                }
                else
                {
                    console.log("successfully replied");
                    return response.json();
                }
            }).then(responseData => {
                if (!responseData['error']) {
                    const gameUrl = '/Game/' + responseData['gameId'] + '/';
                    console.log('setting to -> ', gameUrl);
                    this.#spa.setTo(gameUrl);
                }
                else
                {
                    window.alert(responseData['error']);
                }
            })
        })
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

}