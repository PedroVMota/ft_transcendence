

/*
{'username': 'admin', 'email': 'admin@admin.com', 'first_name': 'None', 'last_name': 'None', 'profile_picture': '/media/Auth/admin/200w_5cM2iEd.webp', 'about_me': 'None', 'create_date': datetime.datetime(2024, 8, 23, 16, 6, 3, 406483, tzinfo=datetime.timezone.utc), 'update_date': datetime.datetime(2024, 8, 23, 16, 13, 26, 772989, tzinfo=datetime.timezone.utc), 'friendlist': []}
*/
document.addEventListener('DOMContentLoaded', function () {
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the default form submission

            const formData = new FormData(this);

            fetch('/Profile/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        console.log(data.message);


                        fetch('/getUserData/', {
                            method: 'GET',
                            headers: {
                                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                            }
                        }
                        ).then(response => response.json())
                        .then(data => {
                            console.log(data);
                            document.getElementById('id_first_name').value = data.user.first_name;
                            document.getElementById('id_last_name').value = data.user.last_name;
                            document.getElementById('id_about_me').value = data.user.about_me;
                            document.getElementById('profilePicture').src = data.user.profile_picture;
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('An error occurred. Please try again.');
                        });






                    } else if (data.error) {
                        console.error(data.error);
                        alert('Error updating profile: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
        });
    }
});