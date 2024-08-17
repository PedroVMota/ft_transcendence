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
    let data = {
        "username": document.getElementById('loginUser').value,
        "password": document.getElementById('loginPassword').value
    };

    fetch('https://localhost:443/auth/token/login/', {
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
        let AccessToken = data.access;
        let RefreshToken = data.refresh;
        localStorage.setItem('Access', AccessToken);
        localStorage.setItem('Refresh', RefreshToken);
        window.location.href = '/'; // Redireciona para a página inicial após o login bem-sucedido
    }).catch(error => {
        console.log(error);
        showAlert('Login failed. Please try again.', 1500);
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
        "password": pass
    };

    fetch('https://localhost:443/auth/token/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.status === 400 || response.status === 500) {
            throw new Error('Registration error');
        }
        return response.json();
    }).then(data => {
        ToggleRegisterToLogin(); // Alterna para o formulário de login após o registro bem-sucedido
        showAlert('Registration successful. Please log in.', 1500);
    }).catch(error => {
        console.error('Error:', error.message);
        showAlert('Registration failed. Please try again.', 1500);
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
