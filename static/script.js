// MyBlog/static/script.js
// Ensures the script runs only after the entire HTML document is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Select all elements with the class 'like-button'
    const likeButtons = document.querySelectorAll('.like-button');

    // Loop through each found button
    likeButtons.forEach(button => {
        // Add a click event listener to each button
        button.addEventListener('click', () => {
            // Get the post ID from the 'data-post-id' attribute on the button
            const postId = button.dataset.postId;
            
            // For now, just show an alert.
            // In a real application, you'd send this postId to your Flask backend
            // using fetch() API or XMLHttpRequest to update the database.
            alert(`You clicked 'Like' for Post ID: ${postId}!`);

            // Optionally, you could disable the button or change its text
            // button.textContent = 'Liked!';
            // button.disabled = true;
        });
    });

    console.log("JavaScript is running!"); // Check your browser's console for this message
});