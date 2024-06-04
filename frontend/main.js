import './style.css'
import { Client, WhenLoggedIn, WhenNotLoggedIn } from './Classes/Client'
export var CurrentClient = new Client();
import { Cookie } from './Classes/Cookie'
import "./Components/Menu";
import $ from 'jquery';


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

document.getElementById('_ProfileManipulationSecion').addEventListener('mouseover', function () {
    console.log('ProfileManipulationSecion');
    /*
        Data Jsong Example :
        {
            "username": "admin",
            "email": "admin@admin.com",
            "profile_image": "/api/defaultAssets/ProfilePicture.png",
            "about_me": null,
            "create_date": "2024-06-04T12:33:38.103Z",
            "update_date": "2024-06-04T13:33:33.598Z"
        },
    */
    JsonData = CurrentClient.getProfile();
    console.log(JsonData);
    $('#aboutMe').text(JsonData['about_me']);


});




document.addEventListener('DOMContentLoaded', () => {

    let  _loginSubmission = document.getElementById('_loginSubmission');
    let  _registerSubmission = document.getElementById('_registerSubmission');

    let  Session = new Cookie();
    if (Session.isSessionLoggedIn()) {
        console.log('Session is logged in');
        WhenLoggedIn();
    }
    else {
        console.log('Session is not logged in');
        WhenNotLoggedIn();
    }
    // LOGIN
    _loginSubmission.addEventListener('click', (event) => {
        event.preventDefault();
        CurrentClient.login();
    });
    // RESITER
    _registerSubmission.addEventListener('click', (event) => {
        event.preventDefault();
        CurrentClient.register();
    });
    
    $('#_Logout').on('click', function () {
        CurrentClient.logout();
    });

    var _ProfileManipulationSecion = document.getElementById('_ProfileManipulationSecion');
    CurrentClient.getProfile().then(data => {
        console.log(">>>>>>>>>", _data);
    });

});



