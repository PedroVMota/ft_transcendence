import { Cookie } from "./Cookie";
import $ from 'jquery';


export function WhenLoggedIn() {
    console.log('WhenLoggedIn');
    let _WhenNotLoggedIn = document.getElementById('_WhenNotLoggedIn');
    let _WhenLoggedIn = document.getElementById('_WhenLoggedIn');

    _WhenNotLoggedIn.classList.remove('d-flex');
    _WhenNotLoggedIn.style.display = 'none';
    _WhenLoggedIn.classList.remove('d-none');



    $('._Username').text(localStorage.getItem('Username').toUpperCase());

}

export function WhenNotLoggedIn() {
    console.log('WhenNotLoggedIn');
    let _WhenNotLoggedIn = document.getElementById('_WhenNotLoggedIn');
    let _WhenLoggedIn = document.getElementById('_WhenLoggedIn');
    _WhenNotLoggedIn.classList.add('d-flex');
    _WhenNotLoggedIn.style.display = 'block';
    _WhenLoggedIn.classList.add('d-none');
    _WhenLoggedIn.style.display = 'block';
}

export class Client {
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


    loadClient() {
        console.log('Loading client');
        self.Username = localStorage.getItem('Username');
        self.Email = localStorage.getItem('Email');
        self.is_staff = localStorage.getItem('is_staff');
        self.is_superuser = localStorage.getItem('is_superuser');
    }

    login() {
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
                password: password.value,
                is_staff: true,
                is_superuser: true
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
                this.setUsername(data.Username);
                this.setEmail(data.Email);
                this.setIsStaff(data.is_staff);
                this.setIsSuperuser(data.is_superuser);
                localStorage.setItem('Username', data.Username);
                localStorage.setItem('Email', data.Email);
                localStorage.setItem('is_staff', data.is_staff);
                localStorage.setItem('is_superuser', data.is_superuser);
                WhenLoggedIn();
            })
            .catch((error) => {
                console.error('Error:', error);
            });

    }

    logout() {
        fetch('http://localhost:8000/logout', {
            method: 'POST',
            credentials: 'include',
        })
            .then(response => {
                if (!response.ok) return response.json().then(data => { throw new Error(data.error); });
                return response.json();
            })
            .then(data => {
                Cookie.delete('csrftoken');
                Cookie.delete('sessionid');
                Cookie.deleteLocalStorage();
                WhenNotLoggedIn();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
    register(){
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
                is_staff: true,
                is_superuser: true,
                is_active: true
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
    }

    getProfile() {

        console.log('Getting profile');
        fetch('http://localhost:8000/UserDetails', {
            method: 'GET',
            credentials: 'include',
        })
            .then(response => {
                if (!response.ok) return response.json().then(data => { throw new Error(data.error); });
                return response.json();
            })
            .then(data => {
                // console.log(data);
                return data;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
}

