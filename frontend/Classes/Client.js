import { Cookie } from "./Cookie";


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
                this.setUsername(data.Username);
                this.setEmail(data.Email);
                this.setIsStaff(data.is_staff);
                this.setIsSuperuser(data.is_superuser);
                localStorage.setItem('Username', data.Username);
                localStorage.setItem('Email', data.Email);
                localStorage.setItem('is_staff', data.is_staff);
                localStorage.setItem('is_superuser', data.is_superuser);
                
                AfterLogin();
                let div = document.querySelector('._AfterLogin');
                div.style.display = 'none';


            })
            .catch((error) => {
                console.error('Error:', error);
            });

            setInterval(() => {
                console.log('Username:', this.getUsername());
                console.log('Email:', this.getEmail());
                console.log('is_staff:', this.getIsStaff());
                console.log('is_superuser:', this.getIsSuperuser());

            }, 1000);
    }

    logout() {
        fetch('http://localhost:8000/logout', {
            method: 'POST',
            credentials: 'include',
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
                Cookie.delete('csrftoken');
                Cookie.delete('sessionid');
                Cookie.deleteLocalStorage();
                console.log(data);
                MustBeLoggedIn();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
}

