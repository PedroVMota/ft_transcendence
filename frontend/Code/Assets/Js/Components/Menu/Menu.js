import { login } from '../Login'
import { Color } from '../../Utils/Color'
import { ul, li, Button, ahref } from '../../Utils/Library';

//<button type="button" class="btn btn-outline-light me-2" id="logoutButton">Logout</button>




function logout () {
    console.log('Logout');
    window.history.pushState({}, '', '/');
    document.body.innerHTML = '';
    localStorage.removeItem('Access');
    localStorage.removeItem('Refresh');
    login();
};

// Function to handle navigation without reloading the page
function navigate(event, path) {
    event.preventDefault(); // Prevent the default anchor behavior
    history.pushState({}, '', path); // Change the URL without reloading the page
    // Here, you would also handle changing the view within your SPA
}

function callback(element) {
    element.innerHTML = 'CHANGED';
}




export function Menu(parentElement) {
    const nav = document.createElement('header');

    nav.classList.add('p-3', 'text-bg-white');
    nav.style.backdropFilter = 'blur(2px)';
    nav.style.backgroundColor = `${Color.HexToRGBA('#004e92', 0.5)}`;
    nav.innerHTML = `
            <div class="container">
            <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
                <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none">
                    <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap"><use xlink:href="#bootstrap"></use></svg>
                </a>
                <ul id="ullist" class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
                </ul>
                
                <div class="text-end" id="_RenderAButton" >
                </div>
            </div>
        </div>
    `;
    const lists = ['Home', 'Lobby','Lobby','Lobby','Lobby','Lobby','Lobby',]
    const _ul = new ul()
    _ul.setElement(nav.querySelector('#ullist'));
    for (const list of lists) {
        const _li = new li('nav-item');
        // _li.setInnerHTML(`<a href="/${list.toLowerCase()}" class="nav-link px-2 text-white" onclick="navigate(event, '/${list.toLowerCase()}')">${list}</a>`)
        console.log(lists)
        _li.setText(list);
        _li.setFunction('click', (event) => {
            navigate(event, `/${list.toLowerCase()}`);
        });
        _li.addClass('nav-item');
        _ul.appendChild(_li.get())
    }

    parentElement.appendChild(nav);
    //Creating the button
    const renderButtonDiv = nav.querySelector('#_RenderAButton');
    // Create a instance of the Button class
    const logoutButton = new Button();
    // Apply the text of the button
    logoutButton.setText('Logout'); // Set the button text
    logoutButton.addClass('btn', 'btn-outline-light', 'me-2'); // Set the button class
    logoutButton.setFunction('click', () => {
        callback(renderButtonDiv);
        logout();
    });
    logoutButton.setFunction('mouseover', () => {
        logoutButton.addClass('btn-outline-dark');
    });
    logoutButton.setFunction('mouseout', () => {
        logoutButton.removeClass('btn-outline-dark');
    });
    renderButtonDiv.appendChild(logoutButton.element); // Append the button to the div
    parentElement.appendChild(nav);
}