document.addEventListener('DOMContentLoaded', function() {
    
    // Like/Unlike Post (already existing)
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const url = this.dataset.urlLike;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // CSRF token for security
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log("Post like/unlike:", data);

                const likeCountSpan = document.getElementById(`likes-count-${postId}`);
                likeCountSpan.innerText = data.likes_count;

                if (data.liked) {
                    this.classList.add('btn-success');
                    this.classList.remove('btn-outline-primary');
                    this.innerHTML = `Unlike (<span id="likes-count-${postId}">${data.likes_count}</span>)`;
                } else {
                    this.classList.remove('btn-success');
                    this.classList.add('btn-outline-primary');
                    this.innerHTML = `Like (<span id="likes-count-${postId}">${data.likes_count}</span>)`;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Follow/Unfollow User
    const followBtn = document.querySelector('#follow-btn');

    if (followBtn) {
        followBtn.addEventListener('click', function() {
            const username = this.dataset.username;
            const url = `/profile/${username}/follow`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // CSRF token for security
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log("Follow/unfollow status:", data);

                // Update the button appearance and text based on the follow/unfollow status
                if (data.is_following) {
                    followBtn.classList.add('btn-success');
                    followBtn.classList.remove('btn-outline-primary');
                    followBtn.innerHTML = `Unfollow (<span id="follower-count">${data.follower_count}</span>)`;
                } else {
                    followBtn.classList.remove('btn-success');
                    followBtn.classList.add('btn-outline-primary');
                    followBtn.innerHTML = `Follow (<span id="follower-count">${data.follower_count}</span>)`;
                }

                // Update the follower count dynamically
                const followerCountSpan = document.querySelector('#follower-count');
                followerCountSpan.innerText = data.follower_count;
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Edit Post Functionality
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const postContent = document.getElementById(`post-content-${postId}`);
            const originalContent = postContent.innerText;

            // Disable the edit button after entering edit mode
            this.disabled = true;

            // Replace the post content with a textarea to allow editing
            postContent.innerHTML = `
                <textarea id="edit-textarea-${postId}" class="form-control textarea-custom" rows="3">${originalContent}</textarea>
                <div class="edit-controls">
                    <button class="btn btn-sm btn-primary save-btn mt-3" data-post-id="${postId}">Save</button>
                    <button class="btn btn-sm btn-secondary cancel-btn mt-3" data-post-id="${postId}">Cancel</button>
                </div>
            `;

            // Handle Save Button Click
            document.querySelector(`.save-btn[data-post-id="${postId}"]`).addEventListener('click', function() {
                const newContent = document.getElementById(`edit-textarea-${postId}`).value;
                fetch(`/posts/${postId}/edit`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')  // CSRF token for security
                    },
                    body: JSON.stringify({
                        content: newContent
                    })
                })
                .then(response => response.json())
                .then(result => {
                    if (result.message === "Post updated successfully.") {
                        // Update the post content and re-enable the edit button
                        postContent.innerHTML = newContent;
                        button.disabled = false;
                    } else {
                        console.error("Error updating post:", result);
                    }
                })
                .catch(error => console.error('Error:', error));
            });

            // Handle Cancel Button Click
            document.querySelector(`.cancel-btn[data-post-id="${postId}"]`).addEventListener('click', function() {
                // Restore only the original content, without any extra HTML, and re-enable the edit button
                postContent.innerHTML = originalContent;
                button.disabled = false;
            });
        });
    });


    // CSRF token handling
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
