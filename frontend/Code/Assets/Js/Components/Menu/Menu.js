import { login } from '../Login'
import { Color } from '../../Utils/Color'
import { ul, li, HTML_PROPS } from '../../Utils/UlLibrary';



function logout () {
    window.history.pushState({}, '', '/');
    document.body.innerHTML = '';
    localStorage.removeItem('Access');
    localStorage.removeItem('Refresh');
    login();
};

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

                <div class="text-end">
                    <button type="button" class="btn btn-outline-light me-2" id="logoutButton">Logout</button>
                </div>
            </div>
        </div>
    `;
    const lists = ['Home', 'Lobby',]
    const _ul = new ul()
    _ul.setElement(nav.querySelector('#ullist'));

    for (const list of lists) {
        const _li = new li('nav-item');
        _li.setInnerHTML(`<a href="/${list.toLowerCase()}" class="nav-link px-2 text-white">${list}</a>`)
        _ul.appendChild(_li.get())
    }

    parentElement.appendChild(nav);

    const logoutButton = nav.querySelector('#logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }
}