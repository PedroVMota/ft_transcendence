import { showAlert } from "./Alert";
import { login } from "./Login";
import { treeJSAplication } from "../treeJSAplication";
import { Menu } from "./Menu/Menu";
import { Color } from "../Utils/Color";

/*
    * Function to render the login page
*/
export function app() {
    var _AppLogin = document.getElementById('_AppLogin');
    if (_AppLogin) {
        _AppLogin.remove();
    }

    var _App = document.createElement('div');
    _App.id = '_App';
    // _App.style.background = Color.LinearGradient(45, Color.RGBToRGBA(60,60,255, 0.8), Color.RGBToRGBA(60,60,255, 0.8));
    _App.style.background = 'url("https://wallpapercave.com/wp/wp3837751.jpg")';
    _App.style.backgroundSize = 'cover';
    _App.style.backgroundPosition = 'center';
    // _App.style.filter = 'blur(5px)';
    console.log(_App.style.background);
    document.body.appendChild(_App);
    
    Menu(_App);

    // if (!document.getElementById('logoutButton')) {
    //     var logoutButton = document.createElement('button');
    //     logoutButton.id = 'logoutButton';
    //     logoutButton.textContent = 'Logout';
    //     logoutButton.addEventListener('click', function () {
    //        
    //     });

        // _App.body.appendChild(logoutButton);
    // }
// 
    // var heading = document.createElement('h1');
    // heading.textContent = 'Welcome to the app!';
    // document.body.appendChild(heading);
// 
    // var paragraph = document.createElement('p');
    // paragraph.textContent = 'This is some more content on the page.';
    // document.body.appendChild(paragraph);
// 
    // Ensure the canvas is added after the paragraph
    // var canvasContainer = document.createElement('div');
    // canvasContainer.id = 'canvasContainer';
    // document.body.appendChild(canvasContainer);
// 
    // Modify treeJSAplication to accept a container element for the renderer
    // treeJSAplication(canvasContainer);
}