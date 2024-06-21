import { login } from '../Login'
import { Color } from '../../Utils/Color'
import { ul, li, Button, ahref } from '../../Utils/Library';

//<button type="button" class="btn btn-outline-light me-2" id="logoutButton">Logout</button>




function logout() {
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

    nav.classList.add('p-3', 'text-white', 'fixed-top');
    nav.style.backdropFilter = 'blur(2px)';
    nav.style.backgroundColor = `${Color.HexToRGBA(Color.RGBToHex(230, 230, 230), 1)}`;
    // nav.style.backgroundColor = `${Color.HexToRGBA('#fefefe', 0.5)}`;
    nav.innerHTML = `
        <div class="container h-full">
            <div class="d-flex align-items-center justify-content-between">


                <button type="button" class="btn btn-outline-none d-flex align-items-center align-items-center" id="logoButton" data-bs-toggle="collapse" data-bs-target="#menuCollapse">
                    <!-- <img src="./Assets/Images/Images/Logo.png" alt="Logo" width="60" height="60"> -->
                    <!--<b>Pong<b>-->
                   <i class="bi bi-list fs-3"></i>
                </button>


                <div class="text-end" id="_RenderAButton">
                    <button type="button" class="btn me-2" id="logoutButton">Logout</button>
                </div>
            </div>

            
            <div class="collapse" id="menuCollapse" style="position: fixed; top: 0; left: 0; height: 100vh; width: 250px;">
                <header class="p-3 text-black d-flex justify-content-end">
                    <i class="bi bi-x fs-1" data-bs-toggle="collapse" data-bs-target="#menuCollapse"></i>
                </header>


            </div>
        </div>
    `;
    parentElement.appendChild(nav);
    document.getElementById('logoutButton').style.color = `${Color.HexToRGBA('#ffffff', 1)}`;
    document.getElementById('logoutButton').style.backgroundColor = `${Color.HexToRGBA(Color.RGBToHex(230, 75, 75), 1)}`;
    document.getElementById('logoutButton').addEventListener('click', logout);
}