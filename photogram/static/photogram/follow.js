document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#followButton').addEventListener('click', follow_user);
    is_following(); // Check if the current profile user is been followed and display the right button for the 'follow/unfollow'
    
})



// Function from Django documentation to acquire the token
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
const csrftoken = getCookie('csrftoken');



// Function to follow user
function follow_user() {
    username = document.querySelector('#username').textContent;

    const request = new Request(
        `/follow/${username}/`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {
        method: 'POST',
        mode: 'same-origin'
    })
        .then(response => response.json())
            .then(result => {
                // Print error message
                console.log(result);
    });

    // Change the button text
    buttonText = document.querySelector('#followButton');
    if (buttonText.innerHTML === 'Follow') buttonText.innerHTML = 'Unfollow';
    else buttonText.innerHTML = 'Follow';
   
}

// Check if the currente profile user is being followed
function is_following() {
    username = document.querySelector('#username').textContent;

    const request = new Request(
        `/follow/${username}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {
        method: 'GET',
        mode: 'same-origin'
    })
        .then(response => response.json())
            .then(result => {
                // Print error message
                console.log(result);
                if (result['is being followed']) {
                    document.querySelector('#followButton').innerHTML = 'Unfollow'
                }
                else {
                    document.querySelector('#followButton').innerHTML = 'Follow'
                }
    });
}