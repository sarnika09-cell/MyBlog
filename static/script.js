document.addEventListener('DOMContentLoaded', () => {
    
    const likeButtons = document.querySelectorAll('.like-button');

    
    likeButtons.forEach(button => {
        
        button.addEventListener('click', () => {
            
            const postId = button.dataset.postId;
           
            alert(`You clicked 'Like' for Post ID: ${postId}!`);

            // Optionally, you could disable the button or change its text
            // button.textContent = 'Liked!';
            // button.disabled = true;
        });
    });

    console.log("JavaScript is running!"); // Check your browser's console for this message
});
