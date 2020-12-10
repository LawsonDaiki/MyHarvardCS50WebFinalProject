document.addEventListener('DOMContentLoaded', function() {

    // Add click event listener to every comment button with it's specific post id
    document.querySelectorAll('#submitComment').forEach(button => {
        
        button.onclick = function() {
            event.preventDefault()
            submitComment(this.dataset.postid)
        }
    })

    // Add click event listener to every showComment button with it's specific post id
    document.querySelectorAll('.showComments').forEach(button => {
        button.onclick = function() {
            // Get comments container element
            let commentsContainer = document.querySelector(`.comments-container[data-postid='${this.dataset.postid}']`);
            commentSubmit = document.querySelector(`.comment-submit[data-postid='${this.dataset.postid}']`);
            if (commentSubmit.style.display === "none" || commentSubmit.style.display === "") {
                getComments(this.dataset.postid);
                commentSubmit.style.display = "block";
            }
            else {
                commentsContainer.innerHTML = '';
                commentSubmit.style.display = "none";
            }
        }
    })
    
})



// Function to like the post

function submitComment(postId) {

    // Get comment text from the DOM
    input = document.querySelector(`#comment[data-postid='${postId}']`);
    inputComment = input.value;

    // Convert comment to a JSON
    let comment = { comment: inputComment }
    comment = JSON.stringify(comment)
    console.log(comment)

    fetch(`/comment/${postId}`, {
        method: 'POST',
        body: comment,
        headers: { 'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        "X-CSRFToken": csrftoken },
    })
        .then(response => response.json().then(data => ({status: response.status, body: data})))
        .then(result => {
            console.log(result.status)
            // Print message
            if (result.status === 201) {
                console.log(result.body.message);
                input.value = '';
                updateComments(postId);
            }
            else {
                console.log(result);
            }
        });
}

function getComments(postId) {

    fetch(`/comment/${postId}`, {
        method: 'GET'
    })
    .then(response => response.json().then(data => ({status: response.status, body: data})))
    .then(result => {
        // Print result message
        console.log(result.status)
        // Print message
        if (result.status === 201) {
            displayComments(JSON.parse(result.body), postId);
        }
        else {
            console.log(result);
        }
    });
}

function displayComments(comments, postId) {

    // Get DOM comment container
    commentsContainer = document.querySelector(`.comments-container[data-postid='${postId}']`);

    for (var key in comments) {

        // Create elements

        const user = document.createElement('p');
        user.innerText = `${comments[key].user}: `;
        user.className = 'commentator'

        const comment = document.createElement('p');
        comment.innerText = `${comments[key].comment}`;
        comment.className = 'comment'

        // Append elements
        const commentContainer = document.createElement('div');
        commentContainer.className = 'comment-container'
        commentContainer.appendChild(user);
        commentContainer.appendChild(comment);

        commentsContainer.appendChild(commentContainer);
    }

    
}

function updateComments(postId) {

    // Get DOM comment container
    commentsContainer = document.querySelector(`.comments-container[data-postid='${postId}']`);
    commentsContainer.innerHTML = '';

    getComments(postId);

    return;
}