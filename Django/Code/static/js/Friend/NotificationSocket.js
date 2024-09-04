
import AWebChat from "../Utils/ASocket.js";


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

        // Send a ping every 2 seconds.
        setInterval(() => {
            console.log('Sending ping to server');
            this._ws.send('ping');
        }, 2000);
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

export default WebSocketClient;