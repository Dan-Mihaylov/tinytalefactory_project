document.addEventListener('DOMContentLoaded', function() {
    let closeButton = document.getElementById('close-messages-button');
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            let messagesContainer = document.getElementById('messages-container');
            if (messagesContainer) {
                messagesContainer.style.transition = 'opacity 1s ease-out';
                messagesContainer.style.opacity = 0;
                setTimeout(function (){
                   messagesContainer.style.display = 'none';
                }, 500);
            }
        });
    }
});
