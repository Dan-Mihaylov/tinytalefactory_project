const totalPages = document.querySelectorAll('.content-swappable');
const dotElements = document.querySelectorAll('.dot');
const xButtonEl = document.querySelector('body > i:first-of-type');

xButtonEl.addEventListener('click', () => history.back());

let pageIndex = 0;
showPage(pageIndex);

function previous(event) {
    pageIndex - 1 < 0 ? pageIndex = totalPages.length - 1 : pageIndex = pageIndex - 1;
    showPage(pageIndex);
}

function next(event) {
    pageIndex + 1 === totalPages.length ? pageIndex = 0 : pageIndex = pageIndex + 1;
    showPage(pageIndex);
}

function showPage(index) {
    resetPages();
    resetDots();

    totalPages[index].style.display = 'flex';
    dotElements[index].classList.add('active');

}

function resetPages() {
    [...totalPages].map(el => el.style.display = 'none');
}

function resetDots() {
    [...dotElements].map(el => el.classList.remove('active'));
}

for (let i = 0; i < dotElements.length; i++) {
    dotElements[i].setAttribute('data-index', i);
    dotElements[i].addEventListener('click', (e) => {
        pageIndex = Number(e.target.getAttribute('data-index'));
        showPage(pageIndex);
    })
}


