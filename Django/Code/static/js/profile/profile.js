// document.addEventListener('DOMContentLoaded', function () {
//     const profileForm = document.getElementById('profileForm');

//     // Function to populate the form with user data
//     function loadUserData() {
//         fetch('/getUserData/', {
//             method: 'GET',
//             headers: {
//                 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
//             }
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(userData => {
//             // Populate form fields with the user data
//             document.getElementById('id_first_name').value = userData.user.first_name;
//             document.getElementById('id_last_name').value = userData.user.last_name;
//             document.getElementById('id_about_me').value = userData.user.about_me;
//             document.getElementById('profilePicture').src = userData.user.profile_picture;
//         })
//         .catch(error => {
//             console.error('Error fetching user data:', error);
//             alert('An error occurred while loading your profile data. Please try again.');
//         });
//     }

//     // Load user data when the page loads
//     loadUserData();

//     if (profileForm) {
//         profileForm.addEventListener('submit', function (event) {
//             event.preventDefault(); // Prevent the default form submission

//             const formData = new FormData(profileForm);

//             fetch('/Profile/', {
//                 method: 'POST',
//                 body: formData,
//                 headers: {
//                     'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
//                 }
//             })
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then(data => {
//                 if (data.message) {
//                     alert(data.message); // Display success message

//                     // Optionally reload the updated user data
//                     loadUserData();
//                 } else if (data.error) {
//                     alert('Error updating profile: ' + data.error); // Display error message
//                 }
//             })
//             .catch(error => {
//                 console.error('Error during fetch:', error);
//                 alert('An error occurred. Please try again.');
//             });
//         });
//     }
// });


// // forcing loading


import AComponent from "../Spa/AComponent.js";
import spa from "../Spa/Spa.js";
import { getCookie, Requests } from "../Utils/Requests.js";


export default class Profile extends AComponent {
    #parentElement = null;
    #spaObject = null;

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
    }

    render() {
        let url = this.getUrl();
        // Display pending message
        this.showSpinner();

        this._getHtml(url).then((html) => {
        let documentResponse = new DOMParser().parseFromString(html, 'text/html');
            let rootContentHtml = documentResponse.getElementById('root').innerHTML;
            if(!(!rootContentHtml)){
                document.head.innerHTML = documentResponse.head.innerHTML;
                


                
                
                
                



                this.#parentElement.innerHTML = rootContentHtml;
                document.getElementById('profileForm').addEventListener('submit', (event) => this.#updateProfile(event));
                this.#loadData();


                setTimeout(() => {
                    this.hideSpinner();
                }, 1000);


            }
        }).catch((error) => {
            
            console.error(error);
        });
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

    #loadData() {

        Requests.get('/getUserData/').then((userData) => {
            // userData = userData.user;
            document.getElementById('id_first_name').value = userData.user.first_name ? userData.user.first_name : 'Empty';
            document.getElementById('id_last_name').value = userData.user.last_name ? userData.user.last_name : 'Empty';
            document.getElementById('id_about_me').value = userData.user.about_me ? userData.user.about_me : 'Empty';
            document.getElementById('profilePicture').src = userData.user.profile_picture;
        })
    }

    #updateProfile(event) {
        event.preventDefault();
        const formData = new FormData(document.getElementById('profileForm'));
        fetch('/Profile/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    this.#loadData();
                } else if (data.error) {
                    alert('Error updating profile: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error during fetch:', error);
                alert('An error occurred. Please try again.');
            });
    }
}

