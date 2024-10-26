class AWebChat {
    _ws = null;
    constructor(url) {
        this._ws = new WebSocket(url);
    }

    connect() {
        this._ws.onopen = this.onOpen;
        this._ws.onmessage = this.onMessage;
        this._ws.onclose = this.onClose;
        this._ws.onerror = this.onError;
    }

    sendMessage(data) {
        throw new Error('Method not implemented -> sendMessage');
    }

    onMessage() {
        throw new Error('Method not implemented -> onMessage');
    }

    onOpen() {
        throw new Error('Method not implemented -> onOpen');
    }

    onClose() {
        throw new Error('Method not implemented -> onClose');
    }

    onError() {
        throw new Error('Method not implemented -> onError');
    }
}

export default AWebChat;