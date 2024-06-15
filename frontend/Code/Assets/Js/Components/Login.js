import { showAlert } from "./Alert";
import { app } from "./App";

/**
 * Toggles the visibility of the login and registration forms by fading out the login form and fading in the registration form.
 * It also hides the login form after the fade-out animation and shows the registration form after the fade-in animation.
*/
const ToggleRegisterToLogin = () => {
    const loginContainer = document.getElementById('loginContainer');
    const registerContainer = document.getElementById('registerContainer');

    registerContainer.classList.add('fade-out');
    setTimeout(() => {
        registerContainer.classList.add('hidden');
        registerContainer.classList.remove('fade-out');
        loginContainer.classList.remove('hidden');
        loginContainer.classList.add('fade-in');
    }, 500);
}

/**
 * Toggles the view from the login form to the registration form by fading out the login form and fading in the registration form.
 * It also hides the login form after the fade-out animation and shows the registration form after the fade-in animation.
*/
const ToggleLoginToRegister = () => {
    const loginContainer = document.getElementById('loginContainer');
    const registerContainer = document.getElementById('registerContainer');

    loginContainer.classList.add('fade-out');
    setTimeout(() => {
        loginContainer.classList.add('hidden');
        loginContainer.classList.remove('fade-out');
        registerContainer.classList.remove('hidden');
        registerContainer.classList.add('fade-in');
    }, 500);
}


/**
 * Renders the login and registration forms on the page. It handles the creation and removal of these forms dynamically.
 * It also sets up event listeners for form submissions and link clicks to toggle between login and registration forms.
 * The login form submission is handled to authenticate users by sending their credentials to a server and storing received tokens.
 * The registration form submission is handled to register new users by sending their details to a server.
 * Additionally, it provides functionality to switch views between the login and registration forms.
 */
export function login() {
    console.log("Login");
    if (document.getElementById('_appAfterLogin')) {
        var _appAfterLogin = document.getElementById('_appAfterLogin');
        _appAfterLogin.classList.add('hidden');
        _appAfterLogin.classList.remove('fade-out');
        _appAfterLogin.remove();
    }
    var _AppLogin = document.createElement('div');
    // Apply the id _AppLogin
    _AppLogin.id = '_AppLogin';
    _AppLogin.innerHTML = `
    <div class="page-container" id="_AppLogin">
    <div class="container-md login-container" id="loginContainer">
        <div class="row">
          <div class="col-12 text-center login-header">Login</div>
          <div class="col-12">
            <form id="loginForm">
              <div class="form-group mb-3">
                <label for="loginUser"><i class="bi bi-person"></i> Username</label>
                <input type="text" class="form-control" id="loginUser" placeholder="Enter username"
                  autocomplete="username" required>
              </div>
              <div class="form-group mb-3">
                <label for="loginPassword"><i class="bi bi-lock"></i> Password</label>
                <input type="password" class="form-control" id="loginPassword" placeholder="Password"
                  autocomplete="current-password" required>
              </div>
              <div class="form-group form-check">
                <input type="checkbox" class="form-check-input" id="rememberMe">
                <label class="form-check-label" for="rememberMe">Remember me</label>
              </div>
              <button type="submit" class="btn btn-primary w-100">Login</button>
              <div class="additional-options">
                <a href="#" id="forgotPassword">Forgot Password?</a>
                <a href="#" id="showRegisterForm">Register</a>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="container-md register-container hidden" id="registerContainer">
        <div class="row">
          <div class="col-12 text-center register-header">Register</div>
          <div class="col-12">
            <form id="registerForm">
              <div class="form-group mb-3">
                <label for="registerUser"><i class="bi bi-person"></i> Username</label>
                <input type="text" class="form-control" id="registerUser" placeholder="Enter username"
                  autocomplete="username" required>
              </div>
              <div class="form-group mb-3">
                <label for="registerEmail"><i class="bi bi-envelope"></i> Email</label>
                <input type="email" class="form-control" id="registerEmail" placeholder="Enter email" autocomplete="email"
                  required>
              </div>
              <div class="form-group mb-3">
                <label for="registerPassword"><i class="bi bi-lock"></i> Password</label>
                <input type="password" class="form-control" id="registerPassword" placeholder="Password"
                  autocomplete="new-password" required>
              </div>
              <div class="form-group mb-3">
                <label for="registerConfirmPassword"><i class="bi bi-lock"></i> Confirm Password</label>
                <input type="password" class="form-control" id="registerConfirmPassword" placeholder="Confirm password"
                  autocomplete="new-password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100">Register</button>
              <div class="additional-options">
                <a href="#" id="showLoginForm">Back to Login</a>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    `
    document.body.appendChild(_AppLogin);

    document.getElementById('loginForm').addEventListener('submit', function (event) {
        event.preventDefault();
        let data = {
            "username": document.getElementById('loginUser').value,
            "password": document.getElementById('loginPassword').value
        }
        fetch('http://localhost:8000/token/login/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => {
            if (response.status === 400) {
                throw new Error('Invalid credentials');
            }
            return response.json();
        }).then(data => {
            let AcessToken = data.access;
            let RefreshToken = data.refresh;
            localStorage.setItem('Access', AcessToken);
            localStorage.setItem('Refresh', RefreshToken);
            window.history.pushState({}, '', '/dashboard');
            app();
        }).catch(error => {
            console.log(error);
            showAlert('Login failed. Please try again.', 5000);
        });
    });

    document.getElementById('registerForm').addEventListener('submit', function (event) {
        event.preventDefault();
        let pass = document.getElementById('registerPassword').value;
        let pass2 = document.getElementById('registerConfirmPassword').value;

        if (pass !== pass2) {
            alert("Passwords do not match");
            return;
        }
        let data = {
            "username": document.getElementById('registerUser').value,
            "email": document.getElementById('registerEmail').value,
            "password": document.getElementById('registerPassword').value
        }
        fetch('http://localhost:8000/token/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => {
            return response.json();
        }).then(data => {
            ToggleRegisterToLogin();
        }).catch(error => {
            login();
            console.error('Error:', error.message);
            showAlert('Registration failed. Please try again.', 5000);
        });
    });

    document.getElementById('showLoginForm').addEventListener('click', function (event) {
        event.preventDefault();
        ToggleRegisterToLogin();
    })
    document.getElementById('showRegisterForm').addEventListener('click', function (event) {
        event.preventDefault();
        ToggleLoginToRegister();
    });


}
/**
 * Sends a JSON request to a specified URL using fetch API. It is an asynchronous function that returns a promise.
 * 
 * @param {string} url - The URL to send the request to.
 * @param {string} method - The HTTP method to use for the request (e.g., 'POST', 'GET').
 * @param {Object} data - The data to be sent with the request, as a JavaScript object.
 * @returns {Promise} A promise that resolves with the response of the request, parsed as JSON.
 */
async function jsonRequest(url, method, data) {
    let response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    return response.json();
}


/**
 * Sends a request with a bearer token authorization header. This function is used for authenticated requests.
 * It throws an error if the response status is not successful.
 * 
 * @param {string} url - The URL to send the request to.
 * @param {string} method - The HTTP method to use for the request (e.g., 'GET', 'POST').
 * @param {string} token - The bearer token to be used for authorization.
 * @returns {Promise} A promise that resolves with the response of the request, parsed as JSON.
 */
async function bearerRequest(url, method, token) {
    let response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json(); // Assuming the server responds with JSON
}

/**
 * Validates the authentication of the user by checking if an access token exists in localStorage.
 * If the token exists, it makes a request to a server endpoint to validate the token.
 * 
 * @returns {Promise} A promise that resolves with the server's response if the token is valid, or false if no token is found.
 */
export function ValidateAuth() {
    let Access = localStorage.getItem('Access');
    if (!Access) {
        return Promise.resolve(false);
    }
    // Ensure bearerRequest returns a Promise
    return bearerRequest('http://localhost:8000/user/', 'GET', Access);
}
