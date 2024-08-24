const totalPages = document.querySelectorAll('.content-swappable');
const dotElements = document.querySelectorAll('.dot');
const xButtonEl = document.querySelector('body > i:first-of-type');
const saveButtonEl = document.getElementById('save-story');

xButtonEl.addEventListener('click', () => history.back());
saveButtonEl.addEventListener('click', saveStory);

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

async function saveStory(event) {
    const storyBookContainer = document.querySelector('section.generate-book');
    // const bodyEl = document.querySelector('body');
    // bodyEl.innerHTML = '';
    // bodyEl.append(storyBookContainer);

    // storyBookContainer = document.querySelector('section.generate-book');

    const options = {
        margin: 0, // No margin
        filename: 'generated-book.pdf',
        image: { type: 'jpeg', quality: 0.99 },
        html2canvas: {
            scale: 4,
            useCORS: true,
            scrollX: 0,
            scrollY: 0
        },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: {
            mode: ['css', 'legacy'],
            after: '.page', // Page break after each .page class
            avoid: ['.cover-page'] // Avoid breaking inside the cover page
        }
    };

    html2pdf().set(options).from(storyBookContainer).save();
}

