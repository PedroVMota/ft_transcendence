import './style.css'

/*
Login responde
{
    "Username": "c",
    "Email": "newuser@example.com",
    "is_staff": true,
    "is_superuser": true,
    "Headers": {
        "Content-Length": "184",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "csrftoken=hdj1Ciml9hxVE0nQKWJPAsE3LZDIEtcTrZy0QG3a4SqBgwKGhepT4QTvYhUbdEoh",
        "Accept": "*//*",
"User-Agent": "Thunder Client (https://www.thunderclient.com)",
"Host": "127.0.0.1:8000",
"Connection": "close"
}
}
*/

class Client {
    constructor() {
        this.Username = undefined;
        this.Email = undefined;
        this.is_staff = false;
        this.is_superuser = false;
    }
    setUsername(username) { this.Username = username; }
    setEmail(email) { this.Email = email; }
    setIsStaff(is_staff) { this.is_staff = is_staff; }
    setIsSuperuser(is_superuser) { this.is_superuser = is_superuser; }
    getUsername() { return this.Username; }
    getEmail() { return this.Email; }
    getIsStaff() { return this.is_staff; }
    getIsSuperuser() { return this.is_superuser; }
}

class Cookie { 
    constructor() { }
    isSessionLoggedIn() { return document.cookie.includes('csrftoken'); }
    getSession() { return document.cookie; }
    getCSRFToken() { return document.cookie.split('=')[1]; }
}


var CurrentClient = new Client();
var _loginComponent = document.getElementById('_loginComponent');
var _registerComponent = document.getElementById('_registerComponent');
var _loginSubmission = document.getElementById('_loginSubmission');
var _toggleToRegister = document.getElementById('_toggleToRegister');
var _registerSubmission = document.getElementById('_registerSubmission');
var _toggleToLogin = document.getElementById('_toggleToLogin');
var loginRequiredElement = document.querySelectorAll('.loginRequired')
var loginNotRequiredElement = document.querySelectorAll('.loginNotRequired')


document.addEventListener('DOMContentLoaded', () => {

    var Session = new Cookie();
    if (Session.isSessionLoggedIn())
    {
        console.log('Session is logged in');
        loginRequiredElement.forEach(element => {
            console.log(element);
            element.style.display = 'block';
        });
        loginNotRequiredElement.forEach(element => {
            element.style.display = 'none';
        });
    }
    else
    {
        console.log('Session is not logged in');
        _loginComponent.style.display = 'block';

        loginRequiredElement.forEach(element => {
            element.style.display = 'none';
        });
        loginNotRequiredElement.forEach(element => {
            element.style.display = 'block';
        }
        );
    }


    _toggleToRegister.addEventListener('click', () => {
        _loginComponent.style.display = 'none';
        _registerComponent.style.display = 'block';
    });
    _toggleToLogin.addEventListener('click', () => {
        _loginComponent.style.display = 'block';
        _registerComponent.style.display = 'none';
    });

    // LOGIN
    _loginSubmission.addEventListener('click', () => {
        event.preventDefault();
        let user = document.getElementById('loginUser');
        let password = document.getElementById('loginPassword');

        fetch('http://localhost:8000/login', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: user.value,
                password: password.value
            }),
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error);
                    });
                }
                return response.json();
            })
            .then(data => {
                CurrentClient.setUsername(data.Username);
                CurrentClient.setEmail(data.Email);
                CurrentClient.setIsStaff(data.is_staff);
                CurrentClient.setIsSuperuser(data.is_superuser);
                console.log(data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // RESITER
    _registerSubmission.addEventListener('click', () => {
        event.preventDefault();
        let user = document.getElementById('registerUser');
        let email = document.getElementById('registerEmail');
        let password = document.getElementById('registerPassword');
        let confirmPassword = document.getElementById('registerConfirmPassword');

        if (password.value !== confirmPassword.value) {
            console.log('Passwords do not match');
            return;
        }

        fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: user.value,
                email: email.value,
                password: password.value,
            }),
        }).then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error);
                });
            }
            return response.json();
        })
            .then(data => {
                console.log(data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});
