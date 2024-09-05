document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.not-visible');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.remove('not-visible');
                entry.target.classList.add('visible');
                console.log(entry.target.classList)
            } else {
                entry.target.classList.add('not-visible');
                entry.target.classList.remove('visible');
            }
        });
    });

    items.forEach(item => {
        observer.observe(item);
    });
});


