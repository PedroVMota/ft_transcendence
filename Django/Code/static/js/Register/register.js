
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

        // Bind the event listeners to maintain context (`this`)
        // this.#Login.addEventListener('submit', this.#login.bind(this));
        this.#Register.addEventListener('submit', (e) => {
            console.log('Registering');
        });
    }

    #login(e) {
        e.preventDefault();  // Prevent form from refreshing the page

        console.log('Logging in');
        const body = {
            "username": document.getElementById('loginUser').value,  // Corrected input ID for login form
            "password": document.getElementById('loginPassword').value  // Corrected input ID for login form
        };

        // Check if fields are empty
        if (body.username === '' || body.password === '') {
            new Alert('Error', 'All fields are required');
            return;
        }

        // Log the form data in the console (simulate login processing)
        console.log('Form Data:', body);
    }

    #register(e) {
        e.preventDefault();  // Prevent form from refreshing the page

        console.log('Registering');
        const body = {
            "username": document.getElementById('username').value,
            "first_name": document.getElementById('firstName').value,
            "last_name": document.getElementById('lastName').value,
            "password": document.getElementById('password').value
        };

        // Check if fields are empty
        if (body.username === '' || body.first_name === '' || body.last_name === '' || body.password === '') {
            new Alert('Error', 'All fields are required');
            return;
        }

        // Log the form data in the console (simulate registration processing)
        console.log('Form Data:', body);
    }
}

const login = new Login('/Login/', null);
