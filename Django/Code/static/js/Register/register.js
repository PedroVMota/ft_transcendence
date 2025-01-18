
import AComponent from "../Spa/AComponent.js";
import Alert from "../Spa/Alert.js";

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

export default class Login extends AComponent {
    #Login = document.getElementById('loginForm');
    #Register = document.getElementById('registerForm');
    #root = document.getElementById('root');
    #okeyToExcute = true;

    constructor(url, spaObject) {
        super(url, spaObject);
    }

    destroy() {
        if (this.#okeyToExcute)
            this.#root.innerHTML = '';
    }

    render() {
        if (!this.#okeyToExcute)
            return;
        this.#Register.addEventListener('submit', (e) => {
            console.log('Registering');
        });
    }
}

const login = new Login('/Login/', null);
