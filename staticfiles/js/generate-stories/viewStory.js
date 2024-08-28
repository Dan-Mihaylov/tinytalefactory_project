const totalPages = document.querySelectorAll('.content-swappable');
const dotElements = document.querySelectorAll('.dot');
const xButtonEl = document.querySelector('body > i:first-of-type');
const preSaveButtonEl = document.getElementById('pre-save-story');
const saveButtonEl = document.getElementById('save-story');
const mainEl = document.querySelector('main');
const bodyEl = document.querySelector('body');
const scrollEl = document.getElementById('scroll-up');

scrollEl.addEventListener('click', scrollToTop);

let sectionControllerEl;
let sectionGenerateBookEl;

let pageFormat = 'a4';
const pageFormatOptions = {
    'a4': {'width': '210mm', 'height': '297mm', 'formatElements': formatElementsA4},
    'a5': {'width': '148mm', 'height': '209.5mm', 'formatElements': formatElementsA5}
}

xButtonEl.addEventListener('click', () => history.back());
preSaveButtonEl.addEventListener('click', preSaveStory);

let pageIndex = 0;
showPage(pageIndex);

window.onscroll = () => scrollFunction();

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
    clearColorPickerElements();
    clearFontSelectElements();
    clearPageSizeSelectElement();

    const [controllerEl, storyBookContainer] = document.querySelectorAll('section.generate-book');

    console.log(storyBookContainer);

    const options = {
        margin_top: 2, // No margin
        filename: 'generated-book.pdf',
        image: { type: 'jpeg', quality: 0.9 },
        html2canvas: {
            scale: 4,
            useCORS: true,
            scrollX: 0,
            scrollY: 0
        },
        jsPDF: { unit: 'mm', format: pageFormat, orientation: 'portrait' },
        pagebreak: {
            mode: ['css', 'legacy'],
            after: '.page', // Page break after each .page class
            avoid: ['.cover-page'] // Avoid breaking inside the cover page
        }
    };

    html2pdf().set(options).from(storyBookContainer).save().then(() => {
        changeControllerText(controllerEl);
        bringBackColorPickerElements();
        bringBackFontSelectElements();
        bringBackPageSizeSelectElement();
    });
}

function toggleDisplays() {
    toggleMainDisplay();
    toggleControllerDisplay();
    toggleBookDisplay();
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
        setTimeout(() => sectionGenerateBookEl.style.opacity = '100', 1);
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
    saveStoryBtnEl.addEventListener('click', saveStory);
    saveStoryBtnEl.setAttribute('id', 'save-story');
    saveStoryBtnEl.className = 'fa-solid fa-download';
    sectionEl.append(saveStoryBtnEl);

    const goBackBtnEl = document.createElement('i');
    goBackBtnEl.addEventListener('click', goBackToStory);
    goBackBtnEl.setAttribute('id', 'return');
    goBackBtnEl.className = 'fa-solid fa-backward';
    sectionEl.append(goBackBtnEl);

    return sectionEl;
}

function goBackToStory(event){
    clearBodyChildren();
    toggleMainDisplay();
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

    attachColorPicker(coverPageEl);
    attachFontSizeElement(coverPageEl, 6);
    attachPageSizeSelect(coverPageEl);

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
    attachFontSizeElement(pageEl, 1.3);

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
    inputForegroundEl.setAttribute('value', '#032E47');
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

function clearBodyChildren() {
    [...bodyEl.children].slice(3).map(el => el.remove());
}

function clearColorPickerElements() {
    [...document.querySelectorAll('.color-picker')].map(el => el.style.display = 'none');
}

function bringBackColorPickerElements() {
    [...document.querySelectorAll('.color-picker')].map(el => el.style.display = 'block');
}

function clearFontSelectElements() {
    [...document.querySelectorAll('.slider-container')].map(el => el.style.display = 'none');
}

function bringBackFontSelectElements() {
    [...document.querySelectorAll('.slider-container')].map(el => el.style.display = 'flex');
}

function clearPageSizeSelectElement() {
    document.querySelector('.page-size-container').style.display = 'none';
}

function bringBackPageSizeSelectElement() {
    document.querySelector('.page-size-container').style.display = 'flex';
}

function changeControllerText(controllerEl) {
    const message = 'You are successfully saving the generated book. You can go back to the story, customize the ' +
        'styles and download again, or you can click on the X button and go back to the previous page.'

    pEl = controllerEl.querySelector('p');
    pEl.textContent = message;
}

function attachFontSizeElement(pageEl, defaultSize) {
    const sliderContainerEl = document.createElement('div');
    sliderContainerEl.classList.add('slider-container');
    pageEl.append(sliderContainerEl);

    const spanFontSizeEl = document.createElement('span');
    spanFontSizeEl.setAttribute('id', 'smaller');
    spanFontSizeEl.textContent = 'Font size';
    sliderContainerEl.append(spanFontSizeEl);

    const spanMinusEl = document.createElement('span');
    spanMinusEl.textContent = '-';
    sliderContainerEl.append(spanMinusEl);

    const rangeEl = document.createElement('input');
    rangeEl.setAttribute('type', 'range');
    rangeEl.setAttribute('min', '0.7');
    rangeEl .setAttribute('max', '7');
    rangeEl.setAttribute('value', defaultSize);
    rangeEl.setAttribute('id', 'font-size');
    rangeEl.setAttribute('step', '0.1');
    rangeEl.classList.add('slider');
    rangeEl.addEventListener('change', changeFontSize);
    sliderContainerEl.append(rangeEl);


    const spanPlusEl = document.createElement('span');
    spanPlusEl.textContent = '+';
    sliderContainerEl.append(spanPlusEl);
}

function attachPageSizeSelect(pageEl) {
    const pageSizeContainerEl = document.createElement('div');
    pageSizeContainerEl.classList.add('page-size-container');
    pageSizeContainerEl.style.color = 'rgb(2, 42, 71)';
    pageEl.append(pageSizeContainerEl);

    const labelEl = document.createElement('lavel');
    labelEl.setAttribute('for', 'page-size-select');
    labelEl.textContent = 'Page size:';
    pageSizeContainerEl.append(labelEl);

    const selectEl = document.createElement('select');
    selectEl.setAttribute('name', 'page-size');
    selectEl.setAttribute('id', 'page-size-select');
    selectEl.addEventListener('change', changePageSize);
    pageSizeContainerEl.append(selectEl);

    const a4OptionEl = document.createElement('option');
    a4OptionEl.setAttribute('value', 'a4');
    a4OptionEl.textContent = 'A4';
    selectEl.append(a4OptionEl);

    const a5OptionEl = document.createElement('option');
    a5OptionEl.setAttribute('value', 'a5');
    a5OptionEl.textContent = 'A5';
    selectEl.append(a5OptionEl);
}

function changeFontSize(event) {
    const pageEl = event.target.parentNode.parentNode;
    const value = event.target.value + 'rem';

    // TODO... Fix to be more readable

    [...pageEl.children].map(child => {
        if (child.tagName === 'H1') {
            child.style.fontSize = value;
        } else if (child.tagName === 'ARTICLE') {
            [...child.querySelectorAll('p')].forEach(pEl => pEl.style.fontSize = value);
        }
    })
}

function changePageSize(event) {
    const value = event.target.value;

    pageFormat = value;

    const pageWidth = pageFormatOptions[value].width;
    const pageHeight = pageFormatOptions[value].height;
    pageFormatOptions[value].formatElements();

    const pagesElements = Array.from(document.querySelectorAll('.page'));
    pagesElements.map(page => {
        page.style.maxWidth = pageWidth;
        page.style.minHeight = pageHeight;
        page.style.height = pageHeight;
    })
}

function formatElementsA4() {
    const colorPickerElements = Array.from(document.querySelectorAll('.color-picker'));
    colorPickerElements.map(element => {
        element.style.bottom = '2rem';
        element.style.right = '2rem';
        const [backgroundLabel, foregroundLabel] = element.querySelectorAll('label');
        backgroundLabel.textContent = 'Choose your background';
        foregroundLabel.textContent = 'Choose your characters color';
    });

    const fontSizeElements = Array.from(document.querySelectorAll('.slider-container'));
    fontSizeElements.map(element => {
        element.style.bottom = '2rem';
        element.style.left = '2rem';
        element.style.padding = '1rem';

        const inputEl = element.children[2];
        inputEl.style.height = '0.5rem';
    })

    const pageSizeContainerEl = document.querySelector('.page-size-container');
    pageSizeContainerEl.style.padding = '0.5rem';
    pageSizeContainerEl.style.gap = '1rem';
    pageSizeContainerEl.style.top = '2rem';
    pageSizeContainerEl.style.right = '2rem';

}

function formatElementsA5() {
    const colorPickerElements = Array.from(document.querySelectorAll('.color-picker'));
    colorPickerElements.map(element => {
        element.style.padding = '0';
        const [backgroundLabel, foregroundLabel] = element.querySelectorAll('label');
        backgroundLabel.textContent = 'Background color';
        foregroundLabel.textContent = 'Characters color';
    });

    const fontSizeElements = Array.from(document.querySelectorAll('.slider-container'));
    fontSizeElements.map(element => {
        element.style.bottom = '1rem';
        element.style.left = '1rem';
        element.style.padding = '0.7rem';

        const inputEl = element.children[2];
        inputEl.style.height = '0.2rem';
    })

    const pageSizeContainerEl = document.querySelector('.page-size-container');
    pageSizeContainerEl.style.padding = '0.2rem';
    pageSizeContainerEl.style.gap = '0.5rem';
    pageSizeContainerEl.style.top = '1rem';
    pageSizeContainerEl.style.right = '1rem';
}

function scrollFunction() {

    if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        scrollEl.style.display = 'block';
        return;
    }
    scrollEl.style.display = 'none';
}

function scrollToTop(event) {
    document.documentElement.scrollTop = 0;
}

