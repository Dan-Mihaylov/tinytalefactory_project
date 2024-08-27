const totalPages = document.querySelectorAll('.content-swappable');
const dotElements = document.querySelectorAll('.dot');
const xButtonEl = document.querySelector('body > i:first-of-type');
const preSaveButtonEl = document.getElementById('pre-save-story');
const saveButtonEl = document.getElementById('save-story');
const mainEl = document.querySelector('main');
const bodyEl = document.querySelector('body');

let sectionControllerEl;
let sectionGenerateBookEl;

xButtonEl.addEventListener('click', () => history.back());
preSaveButtonEl.addEventListener('click', preSaveStory);

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

// Functionality on saving the story
async function preSaveStory(event) {
    try {
        const response = await fetch(storyRetrieveUrl);
        const data = await response.json();

        if (response.status !== 200) {
            throw new Error('Something went wrong fetching your result');
        }

        sectionControllerEl = generateControllerEl();
        sectionGenerateBookEl = generateBookEl(data);
        toggleDisplays();


    } catch (error) {
        console.error(error);
    }
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
            scale: 5,
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

function toggleDisplays() {
    toggleMainDisplay();
    toggleControllerDisplay(); // TODO: Need to remove the element after the toggle from display to none.
    toggleBookDisplay(); // TODO: The book pages display is FLEX.
}

function toggleMainDisplay() {
    console.log(mainEl.style.display);

    if (mainEl.style.display === 'block') {
        mainEl.style.opacity = '0';
        setTimeout(() => mainEl.style.display = 'none', 500);
        return;
    }

    mainEl.style.display = 'block';
    mainEl.style.opacity = '1';
}

function toggleControllerDisplay() {
    if (!sectionControllerEl) {
        return;
    }

    if (sectionControllerEl.style.display === 'none') {
        sectionControllerEl.style.display = 'block';
        setTimeout(() => sectionControllerEl.style.opacity = '100', 500);
    }
}

function toggleBookDisplay() {
    if (!sectionGenerateBookEl) {
        return;
    }

    if (sectionGenerateBookEl.style.display === 'none') {
        sectionGenerateBookEl.style.display = 'block';
        setTimeout(() => sectionGenerateBookEl.style.opacity = '100', 500);
    }
}

function generateControllerEl() {
    const pMessage = 'Before saving your book to a .pdf file, you can customize each page background and ' +
        'foreground. When you are done customizing just click on the download button.'

    const sectionEl = document.createElement('section');
    sectionEl.className = 'generate-book controller';
    sectionEl.style.opacity = '0';
    sectionEl.style.display = 'none';
    bodyEl.append(sectionEl);

    const pEl = document.createElement('p');
    pEl.textContent = pMessage;
    sectionEl.append(pEl);

    const saveStoryBtnEl = document.createElement('i');
    saveStoryBtnEl.setAttribute('id', 'save-story');
    saveStoryBtnEl.className = 'fa-solid fa-download';
    sectionEl.append(saveStoryBtnEl);

    const goBackBtnEl = document.createElement('i');
    goBackBtnEl.setAttribute('id', 'return');
    goBackBtnEl.className = 'fa-solid fa-backward';
    sectionEl.append(goBackBtnEl);

    return sectionEl;
}

function generateBookEl(bookData) {
    const mainSectionBookEl = document.createElement('section');
    mainSectionBookEl.classList.add('generate-book');
    mainSectionBookEl.style.display = 'none';
    bodyEl.append(mainSectionBookEl);

    // Cover page
    const coverPageEl = document.createElement('section');
    coverPageEl.className = 'page cover-page';
    mainSectionBookEl.append(coverPageEl);

    const headerEl = document.createElement('h1');
    headerEl.setAttribute('id', 'cover-page-header');
    headerEl.textContent = bookData.title;
    coverPageEl.append(headerEl);

    // Other pages
    const paragraphList = bookData.info.paragraphs;
    const urlsList = bookData.info.urls;

    let page = 1;

    for (let i = 0; i < paragraphList.length; i++) {
        const currUrl = urlsList[i];
        const currParagraph = paragraphList[i];

        mainSectionBookEl.append(createPage(currUrl, currParagraph));
    }

    return mainSectionBookEl;
}

function createPage(url, paragraph){
    const pageEl = document.createElement('section');
    pageEl.classList.add('page');

    const articleEl = document.createElement('article');
    articleEl.classList.add('generate-book-container');
    pageEl.append(articleEl);

    const mediaDivEl = document.createElement('div');
    mediaDivEl.classList.add('media');
    articleEl.append(mediaDivEl);

    const imgEl = document.createElement('img');
    imgEl.setAttribute('src', url);
    imgEl.setAttribute('alt', 'image');
    mediaDivEl.append(imgEl);

    const pEl = document.createElement('p');
    pEl.textContent = paragraph;
    articleEl.append(pEl);

    attachColorPicker(pageEl);

    return pageEl;
}

function attachColorPicker(pageEl) {
    const colorPickerDivEl = document.createElement('div');
    colorPickerDivEl.classList.add('color-picker');
    pageEl.append(colorPickerDivEl);

    // Background field
    const backgroundFieldEl = document.createElement('div');
    backgroundFieldEl.classList.add('input-field');
    colorPickerDivEl.append(backgroundFieldEl);

    const labelBackgroundEl = document.createElement('label');
    labelBackgroundEl.setAttribute('for', 'choose-background');
    labelBackgroundEl.textContent = 'Choose your background';
    backgroundFieldEl.append(labelBackgroundEl);

    const inputBackgroundEl = document.createElement('input');
    inputBackgroundEl.addEventListener('change', changeBackground);
    inputBackgroundEl.setAttribute('type', 'color');
    inputBackgroundEl.setAttribute('name', 'background');
    inputBackgroundEl.setAttribute('id', 'choose-background');
    inputBackgroundEl.setAttribute('value', '#ffffff');
    backgroundFieldEl.append(inputBackgroundEl);

    // Foreground field
    const foregroundFieldEl = document.createElement('div');
    foregroundFieldEl.classList.add('input-field');
    colorPickerDivEl.append(foregroundFieldEl);

    const labelForegroundEl = document.createElement('label');
    labelForegroundEl.setAttribute('for', 'choose-foreground');
    labelForegroundEl.textContent = 'Choose your characters color';
    foregroundFieldEl.append(labelForegroundEl);

    const inputForegroundEl = document.createElement('input');
    inputForegroundEl.addEventListener('change', changeForeground);
    inputForegroundEl.setAttribute('id', 'choose-foreground');
    inputForegroundEl.setAttribute('type', 'color');
    inputForegroundEl.setAttribute('name', 'foreground');
    inputForegroundEl.setAttribute('value', '#022a47');
    foregroundFieldEl.append(inputForegroundEl);
}

function changeBackground(event) {
    const pageEl = event.target.parentNode.parentNode.parentNode
    const color = event.target.value;

    pageEl.style.backgroundColor = color;
}

function changeForeground(event) {
    const pageEl = event.target.parentNode.parentNode.parentNode;
    const color = event.target.value;

    pageEl.style.color = color;

    // [...pageEl.children].map(child => child.style.color = target.value);
}










