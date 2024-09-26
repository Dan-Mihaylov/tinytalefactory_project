document.addEventListener('DOMContentLoaded', () => {
    attachRelativeToBodyClass();
});


function attachRelativeToBodyClass() {
    document.querySelector('body').style.position = 'relative';
}