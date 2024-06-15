import { showAlert } from "./Alert";

/*
    * Function to render the login page
*/
export function app() {
    var _AppLogin = document.getElementById('_AppLogin'); // Correctly define _AppLogin
    console.log(_AppLogin); // Log _AppLogin to the console
    if (_AppLogin) {
        _AppLogin.remove();
    }

    // Verifica se o botão de logout já existe
    if (!document.getElementById('logoutButton')) {
        // Cria um botão de logout
        var logoutButton = document.createElement('button');
        logoutButton.id = 'logoutButton';
        logoutButton.textContent = 'Logout';
        logoutButton.addEventListener('click', function () {
            window.history.pushState({}, '', '/'); // Muda a URL para '/'
            // Limpa todo o conteúdo da página
            document.body.innerHTML = '';
            login(); // Chama a função login para renderizar a página de login
        });

        // Adiciona o botão de logout ao body
        document.body.appendChild(logoutButton);
    }

    // Adiciona mais elementos à página
    var heading = document.createElement('h1');
    heading.textContent = 'Welcome to the app!';
    document.body.appendChild(heading);

    var paragraph = document.createElement('p');
    paragraph.textContent = 'This is some more content on the page.';
    document.body.appendChild(paragraph);

    treeJSAplication();
}