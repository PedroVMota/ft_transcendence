
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


// Função para alternar entre os formulários de registro e login
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

// Função simples para mostrar alertas
const showAlert = (message, timeout) => {
    alert(message);
}

// Evento de submissão do formulário de login
document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let loginData = {
        "username": document.getElementById('loginUser').value,
        "password": document.getElementById('loginPassword').value
    };

    fetch('/auth/token/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(loginData),
        credentials: 'include' // This ensures cookies (like the session cookie) are included in requests
    }).then(response => {
        if (response.status === 200) {
            return response.json();
        } else if (response.status === 400) {
            throw new Error('Invalid username or password');
        } else {
            throw new Error('Login failed');
        }
    }).then(data => {
        console.log('Login successful:', data.message);
        Alert.ShowAlert('Login successful', 'alert alert-success alert-dismissible fade show');
        window.location.replace('/');
        // Handle successful login (e.g., redirect to a different page)
        alert
    }).catch(error => {
        console.error('Error:', error.message);
        Alert.ShowAlert(`Login failed. ${error.message}`, 'alert alert-danger alert-dismissible fade show');
        // Handle errors (e.g., display an error message)
    });
});

// Evento de submissão do formulário de registro
document.getElementById('registerForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let pass = document.getElementById('registerPassword').value;
    let pass2 = document.getElementById('registerConfirmPassword').value;

    if (pass !== pass2) {
        showAlert("Passwords do not match", 1500);
        return;
    }

    let data = {
        "username": document.getElementById('registerUser').value,
        "email": document.getElementById('registerEmail').value,
        "password": pass,
        "password2": pass2
    };

    fetch('/auth/token/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')

        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.status === 400 || response.status === 500) {
            throw new Error('Registration error');
        }
        return response.json();
    }).then(data => {
        ToggleRegisterToLogin(); // Alterna para o formulário de login após o registro bem-sucedido
        Alert.ShowAlert('Registration went sucessfully', 'alert alert-success alert-dismissible fade show');
        // showAlert('Registration successful. Please log in.', 1500);

    }).catch(error => {
        console.error('Error:', error.message);
        Alert.ShowAlert(`Registration failed. ${error.message}`, 'alert alert-danger alert-dismissible fade show');
        // showAlert('Registration failed. Please try again.', 1500);
    });
});

// Eventos para alternar entre os formulários
document.getElementById('showLoginForm').addEventListener('click', function (event) {
    event.preventDefault();
    ToggleRegisterToLogin();
});
document.getElementById('showRegisterForm').addEventListener('click', function (event) {
    event.preventDefault();
    ToggleLoginToRegister();
});
