import AComponent from "../Spa/AComponent.js";
import  spa from '../Spa/Spa.js'
import { reloadWindow } from '../Spa/Spa.js'
import { getCookie } from '../Utils/Utils.js'


export default class Home extends AComponent {
    #parentElement = null;
    #spaObject = null;

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
    }

    render() {
        console.log("Rendering Home");
        const url = this.getUrl();
        if(this.#parentElement.innerHTML !== ''){
            return;
        }
        this._getHtml(url)
            .then((html) => {
                let domResponse = new DOMParser().parseFromString(html, 'text/html');
                let rootContentHtml = domResponse.getElementById('root').innerHTML;
                document.head.innerHTML = domResponse.head.innerHTML;
                this.#parentElement.innerHTML = rootContentHtml; // HTML injected here
                this.#setEventHandlers();
            })
            .catch((error) => {
                console.error('Error fetching HTML:', error);
            });

            
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

    #setEventHandlers() {
        const createLobbyButton = document.getElementById('createLobbyForm');
        const joinLobbyButton = document.getElementById('joinLobbyForm');
        createLobbyForm?.addEventListener('submit', (event) => this.handleCreateLobbySubmission(event));
        joinLobbyForm?.addEventListener('submit', (event) => this.handleJoinLobbySubmission(event));
    }

    handleCreateLobbySubmission(event) {
        event.preventDefault();
        const data = {
            'LobbyName': document.getElementById('createName').value,
        };
    
        fetch('/api/lobby/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            spa.setTo(`/Lobby/${data.Lobby.uuid}`);
        })
        .catch(error => {
            console.error('Error creating lobby:', error);
        });
    }
    
    handleJoinLobbySubmission(event) {
        event.preventDefault();
        const data = {
            'LobbyName': document.getElementById('joinName').value,
        };
    
        fetch('/api/lobby/information/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': `{{ csrf_token }}`,
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.Lobby) {
                spa.setTo(`/Lobby/${data.Lobby.uuid}`);
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error joining lobby:', error);
        });
    }
}