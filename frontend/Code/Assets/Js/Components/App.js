import { showAlert } from "./Alert";
import { login } from "./Login";
import { treeJSAplication } from "../treeJSAplication";
import { Menu } from "./Menu/Menu";

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
    _App.classList.add('bg-primary');
    document.body.appendChild(_App);
    
    Menu(_App);

    // if (!document.getElementById('logoutButton')) {
    //     var logoutButton = document.createElement('button');
    //     logoutButton.id = 'logoutButton';
    //     logoutButton.textContent = 'Logout';
    //     logoutButton.addEventListener('click', function () {
    //         window.history.pushState({}, '', '/');
    //         document.body.innerHTML = '';
    //         localStorage.removeItem('Access');
    //         localStorage.removeItem('Refresh');
    //         login();
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