document.addEventListener('DOMContentLoaded', function() {

    // Add click event listener to every like button with it's specific post id
    document.querySelectorAll('.likeButton').forEach(button => {
        button.onclick = function() {
            likePost(this.dataset.postid)
        }
    })
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



// Function to like the post

function likePost(postid) {

    // Get the specific like count
    likeNumberDiv = document.querySelector(`.likeNumber[data-postid='${postid}']`);
    likeNumber = parseInt(likeNumberDiv.innerHTML);

    // Send request to update like number
    const request = new Request(
        `/likePost/${postid}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {
        method: 'POST',
        mode: 'same-origin'
    })
        .then(response => response.json().then(data => ({status: response.status, body: data})))
        .then(result => {
            console.log(result.status)
            // Print message
            if (result.status === 201) {
                console.log(result.body.message)
                if (result.body.message === 'liked') {
                    // Add +1 to like count
                    likeNumber++;

                    // Update value
                    likeNumberDiv.innerHTML = likeNumber;
                }
                else {
                    // Add +1 to like count
                    likeNumber--;

                    // Update value
                    likeNumberDiv.innerHTML = likeNumber;
                }
                
            }
            else {
                console.log('Sorry, you can only like a post once.');
            }
        });
}