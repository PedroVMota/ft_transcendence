import AComponent from "../Spa/AComponent.js";
import { Requests } from "../Utils/Requests.js";

// Helper function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



export default class Friends extends AComponent {
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
        this.#parentElement.innerHTML = '<span>Pending...</span>';

        this._getHtml(url).then((html) => {
            let documentResponse = new DOMParser().parseFromString(html, 'text/html');
            let rootContentHtml = documentResponse.getElementById('root').innerHTML;
            if (rootContentHtml) {
                document.head.innerHTML = documentResponse.head.innerHTML;
                this.#parentElement.innerHTML = rootContentHtml;

                // Initialize search user events
                this.#searchUsersEvents();

                setTimeout(() => {
                    this.hideSpinner();
                }, 1000);
            }
        }).catch((error) => {
            console.error(error);
        });

        this.#test();
    }

    destroy() {
        this.#parentElement.innerHTML = '';
    }

    #test() {
    }

    #searchUsersEvents() {
        const searchInput = document.querySelector('.form-control[placeholder="Search or add a friend..."]');
        const searchButton = document.querySelector('.btn[type="button"]');
        const searchResultsList = document.getElementById('search-results-list');
        console.log(searchInput, searchButton, searchResultsList);

        if (searchButton && searchInput) {
            searchButton.addEventListener('click', () => {
                const userCode = searchInput.value.trim();

                if (userCode === "") {
                    alert("Please enter a search term.");
                    return;
                }

                // Clear previous search results
                searchResultsList.innerHTML = '';

                // Create the search query
                const searchQuery = `/searchUser?user_code=${encodeURIComponent(userCode)}`;

                // Send the request to the server
                fetch(searchQuery, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Add CSRF token if needed
                    }
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        // Handle the server's response here
                        console.log('Search results:', data);
            
                        // Check if friends are returned
                        if (data.friends && data.friends.length > 0) {
                            data.friends.forEach(friend => {
                                // Create an HTML element for each friend in the results
                                const friendItem = document.createElement('a');
                                friendItem.href = '#';
                                friendItem.className = 'list-group-item list-group-item-action d-flex friend-item acrylicStyle';
            
                                friendItem.innerHTML = `
                                    <div class="position-relative">
                                        <img src="${friend.profile_picture}" alt="${friend.username}">
                                        <span class="friend-status status-online position-absolute"></span>
                                    </div>
                                    <div class="friend-info">
                                        <div>${friend.username}</div>
                                        <div class="text-muted small">${friend.email}</div>
                                    </div>
                                `;
            
                                // Append the friend item to the search results list
                                searchResultsList.appendChild(friendItem);
                            });
                        } else if (data.error) {
                            // Show an error message if the user was not found
                            const errorItem = document.createElement('div');
                            errorItem.className = 'text-danger';
                            errorItem.textContent = data.error;
                            searchResultsList.appendChild(errorItem);
                        }
                    })
                    .catch(error => {
                        console.error('Error during search:', error);
                        alert('An error occurred while searching. Please try again.');
                    });
            });
        } else {
            console.error('Search input or button not found');
        }
    }


}