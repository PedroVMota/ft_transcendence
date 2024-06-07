import './style.css'
import { Client, WhenLoggedIn, WhenNotLoggedIn } from './Classes/Client'
export var CurrentClient = new Client();
import { Cookie } from './Classes/Cookie'
// import "./Components/Menu";
import $ from 'jquery';

import { ErrorCompoentJavaScriptVanilla } from './Components/Alerts'


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






document.addEventListener('DOMContentLoaded', () => {

    let _loginSubmission = document.getElementById('_loginSubmission');
    let _registerSubmission = document.getElementById('_registerSubmission');

    let Session = new Cookie();
    if (Session.isSessionLoggedIn()) {
        console.log('Session is logged in');
        WhenLoggedIn();
        $('#_UpdateProfile').attr('src', `http://localhost:8000/pImg`);
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

    // var _ProfileManipulationSecion = document.getElementById('_ProfileManipulationSecion');
    CurrentClient.getProfile().then(data => {
        if(data == null || data == undefined)
            return ;
        $('#aboutMe').text(data['about_me']);
    });

});


$('#_ChangeProfileImage').on('click', function () {

    let Session = new Cookie();
    if (!Session.isSessionLoggedIn()) {
        return;
    }
    var fileInput = $('<input type="file" accept="image/*" style="display: none;">');
    fileInput.on('change', function (event) {
        var file = event.target.files[0];
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#_UpdateProfile').attr('src', e.target.result);
            // Send this file to the server
            fetch(`http://localhost:8000/profile/image/update/${localStorage.getItem('Username')}`, {
                method: 'PUT',
                body: file  // Send the file as raw binary data
            })
                .then(response => response.json())
                .then(data => {
                    if(data['status'] == '400' || data['status'] == '404')
                    {
                        let _ServerResponse = document.getElementById('_ServerResponse');
                        console.log(_ServerResponse);
                        _ServerResponse.appendChild(ErrorCompoentJavaScriptVanilla(data));
                    }
                })
        };
        reader.readAsDataURL(file);
        // Remove the file input element from the body after the file is selected
        fileInput.remove();
    });
    $('body').append(fileInput);
    fileInput.click();
});