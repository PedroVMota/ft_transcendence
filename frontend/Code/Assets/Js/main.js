import { Color } from  './Utils/Color'
import { login } from './Components/Login'
import { app } from './Components/App'
import { treeJSAplication } from './treeJSAplication'


if (localStorage.getItem('Access') === null) {
  login();
}
else {
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