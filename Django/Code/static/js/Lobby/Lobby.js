import AComponent from "../Spa/AComponent.js";
import { reloadWindow } from '../Spa/Spa.js';

console.log("Lobby.js loaded");

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


export default class Lobby extends AComponent {
    #webSocket = null
    #parentElement = null
    #lobbyId = ''
    #spa = null

    constructor(url, spaObject, lobbyID) {
        console.log("Lobby constructor");
        super(url, spaObject);
        let protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        let host = window.location.host;
        // re_path(r'ws/connect/lobby/(?P<lobby_id>[0-9a-f-]{36})/', LobbyConsumer.as_asgi()),
        let path = "/ws/connect/lobby/" + lobbyID + "/";
        this.#webSocket = new WebSocket(`${protocol}://${host}${path}`);
        this.#parentElement = document.getElementById("root");
        this.#lobbyId = lobbyID;
        this.#spa = spaObject;
    }

    render() {
        console.log("Rendering Lobby");
        const url = this.getUrl();
        this._getHtml(url)
            .then((html) => {
                const newDom = new DOMParser().parseFromString(html, 'text/html');
                document.head.innerHTML = newDom.head.innerHTML;
                const root = newDom.getElementById("root");
                this.#parentElement.innerHTML = root.innerHTML;
                console.log("Lobby rendered");
                this.#setWebSocketEventHandlers();
                this.#setEventHandlers();
            })
            .catch((error) => {
            })
    }

    #setWebSocketEventHandlers() {
        console.log("Setting up web socket event handlers");

        this.#webSocket.onopen = function () { };
        this.#webSocket.onmessage = function (event) {
            const message = JSON.parse(event.data);
            if (message.action === 'refresh') {
                reloadWindow();
            }
        };
        this.#webSocket.onerror = function (error) { };
        this.#webSocket.onclose = function () { };
    }


    #setEventHandlers() {
        try {
            this.#SetUpStartGameButton();
            this.#SetUpInviteFriendButton();
            this.#SetUpLeaveGameButton();
            this.#SetUpColorPicker();
        }
        catch (error) {
            console.error(error);
        }
    }


    destroy() {
        this.#parentElement.innerHTML = '';
    }


    #SetUpColorPicker() {
        const colorPicker = document.getElementById('colorPicker');
        const ballColorPicker = document.getElementById('ballColorPicker');
        const savedColor = localStorage.getItem('selectedColor');
        const savedBallColor = localStorage.getItem('ballColor');

        if (!colorPicker || !ballColorPicker)
            throw new Error('Color picker not found or no saved color');

        if (savedColor)
            colorPicker.value = savedColor;
        if (savedBallColor)
            ballColorPicker.value = savedBallColor;

        // Save colors to local storage on change
        colorPicker.addEventListener('input', (event) => {
            localStorage.setItem('selectedColor', event.target.value);
        });
        ballColorPicker.addEventListener('input', (event) => {
            localStorage.setItem('ballColor', event.target.value);
        });
    }

    #SetUpInviteFriendButton() {
        const inviteFriendButton = document.getElementById("invite-friend-button");
        if (!inviteFriendButton) {
            throw new Error('Invite friend button not found');
        }

        inviteFriendButton.addEventListener('click', (event) => {
            console.log("Invite friend button clicked");
            event.preventDefault();
            let userCodeToInvite = window.prompt("Enter the user code of the friend you want to invite");
            console.log(userCodeToInvite);
            if (userCodeToInvite === null || userCodeToInvite === '' || userCodeToInvite === undefined) {
                alert("Invalid user code");
                return;
            }
            const url = `/auth/token/notification/invite/${this.#lobbyId}/`;
            console.log(url);

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    'to': userCodeToInvite
                })
            }).then(response => {
                if (!response.ok)
                    throw new Error('Network response was not ok');
                return response.json();
            }).then(responseData => {

                console.log("Response data Then");
                if (responseData['error'])
                    alert(responseData['error']);
                else
                    alert("Invitation sent");
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while sending the invitation');
            });
        });
    }

    #SetUpLeaveGameButton() {
        const leaveGameButton = document.getElementById("leave-game-button");
        if (!leaveGameButton) {
            throw new Error('Leave game button not found');
        }

        leaveGameButton.addEventListener('click', (event) => {
            console.log("Leave game button clicked");
            event.preventDefault();
            const url = 'api/lobby/leave/';
            const data = {
                'id': this.#lobbyId,
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
                    throw new Error('Network response was not ok');
                return response.json();
            }).then(responseData => {
                this.#webSocket.close();
                this.#spa.setTo("/");
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while leaving the game');
            });
        });
    }
    
    #SetUpStartGameButton() {
        const startGameButton = document.getElementById("start-game-button");
        if (!startGameButton) {
            throw new Error('Start game button not found');
        }

        startGameButton.addEventListener('click', (event) => {
            console.log("Start game button clicked");
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
                    throw new Error('Network response was not ok');
                else
                    return response.json();
            }).then(responseData => {
                if (!responseData['error']) {
                    const gameUrl = '/Game/' + responseData['gameId'] + '/';
                    this.#spa.setTo(gameUrl);
                }
                else
                    window.alert(responseData['error']);
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while starting the game');
            });
        });
    }
}

