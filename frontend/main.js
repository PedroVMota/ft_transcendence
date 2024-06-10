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

document.getElementById('loginForm').addEventListener('submit', function (event) {
  event.preventDefault();
  let data = {
    "username": document.getElementById('loginUser').value,
    "password": document.getElementById('loginPassword').value
  }

  fetch('http://localhost:8000/token/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  }).then(response => {
    return response.json();
  }).then(data => {
    console.log(data);
    // Here you can handle the response, save the tokens, redirect the user, etc.
  }).catch(error => {
    console.error('Error:', error);
  });
});

document.getElementById('registerForm').addEventListener('submit', function (event) {
  event.preventDefault();
  let pass = document.getElementById('registerPassword').value;
  let pass2 = document.getElementById('registerConfirmPassword').value;

  if(pass !== pass2){
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
      // Here you can handle the response, save the tokens, redirect the user, etc.
  }).catch(error => {
      console.error('Error:', error);
  });

  
});