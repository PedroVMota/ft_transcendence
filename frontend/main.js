import './style.css'
import { Client } from './Classes/Client'
export var CurrentClient = new Client();
import { Cookie } from './Classes/Cookie'
import './Classes/Canva'























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


export function MustBeLoggedIn() {
    console.log('You must be logged in to access this page');
    var loginRequiredElement = document.querySelectorAll('.loginRequired')
    var _AfterLoginElement = document.querySelectorAll('._AfterLogin')
    var _loginComponent = document.getElementById('_loginComponent');

    // _loginComponent.style.display = 'block';
    loginRequiredElement.forEach(element => {
        element.style.display = 'none';
    });
    _AfterLoginElement.forEach(element => {
        element.style.display = 'block';
    }
    );
}

export function AfterLogin() {
    // console.log('You are now logged in');
    var loginRequiredElement = document.querySelectorAll('.loginRequired')
    var _AfterLoginElement = document.querySelectorAll('._AfterLogin')
    loginRequiredElement.forEach(element => {
        console.log(element);
        element.style.display = 'block';
    });
    // console.log('_AfterLoginElement is defined');
    // console.log(_AfterLoginElement);
    _AfterLoginElement.forEach(element => {
        console.log("Before: " + element.style.display)
        element.style.display = 'hidden';
        console.log("After: " + element.style.display)
    });
}



var _loginComponent = document.getElementById('_loginComponent');
var _registerComponent = document.getElementById('_registerComponent');
var _loginSubmission = document.getElementById('_loginSubmission');
var _logoutSubmission = document.getElementById('_logoutSubmission');
var _toggleToRegister = document.getElementById('_toggleToRegister');
var _registerSubmission = document.getElementById('_registerSubmission');
var _toggleToLogin = document.getElementById('_toggleToLogin');
// var loginRequiredElement = document.querySelectorAll('.loginRequired')
// var _AfterLoginElement = document.querySelectorAll('._AfterLogin')


document.addEventListener('DOMContentLoaded', () => {

    var Session = new Cookie();
    if (Session.isSessionLoggedIn()) {
        console.log('Session is logged in');
        AfterLogin();
    }
    else {
        console.log('Session is not logged in');
        MustBeLoggedIn();

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
    _loginSubmission.addEventListener('click', (event) => {
        event.preventDefault();
        CurrentClient.login();
    });

    _logoutSubmission.addEventListener('click', (event) => {
        event.preventDefault();
        CurrentClient.logout();
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
