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
    _App.style.height = '100vh';
    // _App.style.background = Color.LinearGradient(45, Color.RGBToRGBA(60,60,255, 0.8), Color.RGBToRGBA(60,60,255, 0.8));
    
    document.body.appendChild(_App);
    Menu(_App);

}