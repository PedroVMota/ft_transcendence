import { login, ValidateAuth } from './Components/Login'
import { app } from './Components/App'
import { treeJSAplication } from './treeJSAplication'


/**
 * Check if the acess token the user is valid, otherwise, toggle the login page
 */
ValidateAuth().then((response) => {
    console.log(response)
    if (response) {
        app()
    } else {
        login()
    }
}
)