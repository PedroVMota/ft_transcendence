
function app() {
  console.log("APP");
  if (document.getElementById('_AppLogin'))
  {
    var _AppLogin = document.getElementById('_AppLogin');
    _AppLogin.classList.add('hidden');
    _AppLogin.classList.remove('fade-out');
    _AppLogin.remove();
  }
  var newApp = document.createElement('div');
  // Apply the id _appAfterLogin
  newApp.id = '_appAfterLogin';
  newApp.innerHTML = `
    <div class="container-md">
      <div class="row">
        <div class="col-12 text-center">
          <h1>Welcome to the Dashboard</h1>
          <button class="btn btn-primary" id="logout">Logout</button>
        </div>
      </div>
    </div>
  </div>
  `
  document.body.appendChild(newApp);
}

function login() {
  if (document.getElementById('_appAfterLogin'))
  {
    var _appAfterLogin = document.getElementById('_appAfterLogin');
    _appAfterLogin.classList.add('hidden');
    _appAfterLogin.classList.remove('fade-out');
    _appAfterLogin.remove();
  }
  var _AppLogin = document.createElement('div');
  // Apply the id _AppLogin
  _AppLogin.id = '_AppLogin';
  _AppLogin.innerHTML = `
  <div class="page-container" id="_AppLogin">
  <div class="container-md login-container" id="loginContainer">
      <div class="row">
        <div class="col-12 text-center login-header">Login</div>
        <div class="col-12">
          <form id="loginForm">
            <div class="form-group mb-3">
              <label for="loginUser"><i class="bi bi-person"></i> Username</label>
              <input type="text" class="form-control" id="loginUser" placeholder="Enter username"
                autocomplete="username" required>
            </div>
            <div class="form-group mb-3">
              <label for="loginPassword"><i class="bi bi-lock"></i> Password</label>
              <input type="password" class="form-control" id="loginPassword" placeholder="Password"
                autocomplete="current-password" required>
            </div>
            <div class="form-group form-check">
              <input type="checkbox" class="form-check-input" id="rememberMe">
              <label class="form-check-label" for="rememberMe">Remember me</label>
            </div>
            <button type="submit" class="btn btn-primary w-100">Login</button>
            <div class="additional-options">
              <a href="#" id="forgotPassword">Forgot Password?</a>
              <a href="#" id="showRegisterForm">Register</a>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="container-md register-container hidden" id="registerContainer">
      <div class="row">
        <div class="col-12 text-center register-header">Register</div>
        <div class="col-12">
          <form id="registerForm">
            <div class="form-group mb-3">
              <label for="registerUser"><i class="bi bi-person"></i> Username</label>
              <input type="text" class="form-control" id="registerUser" placeholder="Enter username"
                autocomplete="username" required>
            </div>
            <div class="form-group mb-3">
              <label for="registerEmail"><i class="bi bi-envelope"></i> Email</label>
              <input type="email" class="form-control" id="registerEmail" placeholder="Enter email" autocomplete="email"
                required>
            </div>
            <div class="form-group mb-3">
              <label for="registerPassword"><i class="bi bi-lock"></i> Password</label>
              <input type="password" class="form-control" id="registerPassword" placeholder="Password"
                autocomplete="new-password" required>
            </div>
            <div class="form-group mb-3">
              <label for="registerConfirmPassword"><i class="bi bi-lock"></i> Confirm Password</label>
              <input type="password" class="form-control" id="registerConfirmPassword" placeholder="Confirm password"
                autocomplete="new-password" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Register</button>
            <div class="additional-options">
              <a href="#" id="showLoginForm">Back to Login</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  `
  document.body.appendChild(_AppLogin);

  document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let data = {
      "username": document.getElementById('loginUser').value,
      "password": document.getElementById('loginPassword').value
    }
    fetch('http://localhost:8000/token/login/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(response => {
      if (response.status === 400) {
        throw new Error('Invalid credentials');
      }
      return response.json();
    }).then(data => {
      let AcessToken = data.access;
      let RefreshToken = data.refresh;
      localStorage.setItem('Access', AcessToken);
      localStorage.setItem('Refresh', RefreshToken);
      app();
    }).catch(error => {
      console.log(error);
    });
  });

  document.getElementById('registerForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let pass = document.getElementById('registerPassword').value;
    let pass2 = document.getElementById('registerConfirmPassword').value;

    if (pass !== pass2) {
      alert("Passwords do not match");
      return;
    }
    let data = {
      "username": document.getElementById('registerUser').value,
      "email": document.getElementById('registerEmail').value,
      "password": document.getElementById('registerPassword').value
    }
    fetch('http://localhost:8000/token/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(response => {
      return response.json();
    }).then(data => {
      console.log(data);
      app();
    }).catch(error => {
      login();
      console.error('Error:', error.message);
    });
  });
  document.getElementById('showRegisterForm').addEventListener('click', function (event) {
    event.preventDefault();
    const loginContainer = document.getElementById('loginContainer');
    const registerContainer = document.getElementById('registerContainer');

    loginContainer.classList.add('fade-out');
    setTimeout(() => {
      loginContainer.classList.add('hidden');
      loginContainer.classList.remove('fade-out');
      registerContainer.classList.remove('hidden');
      registerContainer.classList.add('fade-in');
    }, 500);
  });

  document.getElementById('showLoginForm').addEventListener('click', function (event) {
    event.preventDefault();
    const loginContainer = document.getElementById('loginContainer');
    const registerContainer = document.getElementById('registerContainer');

    registerContainer.classList.add('fade-out');
    setTimeout(() => {
      registerContainer.classList.add('hidden');
      registerContainer.classList.remove('fade-out');
      loginContainer.classList.remove('hidden');
      loginContainer.classList.add('fade-in');
    }, 500);
  });
}


/* ============= CHECK THE LOCALSTORAGE ACESS TOKEN ============= */
document.addEventListener('DOMContentLoaded', function () {
  if (localStorage.getItem('Access') === null) {
    login();
  }
  if (localStorage.getItem('Access') !== null) {
    fetch('http://localhost:8000/token/verify/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "token": localStorage.getItem('Access')
      })
    }).then(response => {
      if (response.status === 200) {
        console.log("THE TOKEN IS VALID");
        return response.json();
      }
      throw new Error('Invalid token');
    }).then(data => {
      console.log(data);
      app();

    }).catch(error => {
      console.log(error);
      login();
    });
  }
});