const mainEl = document.querySelector('.header-container');
const storyTitleEl = document.getElementById('title');
const childNameEl = document.getElementById('name');
const appearanceEl = document.getElementById('appearance');
const storyAboutEl = document.getElementById('about');
const specialEmphasisEl = document.getElementById('special-emphasis');

const wrapperEl = document.createElement('div');

const bookOpenReaderClass = 'fa-solid fa-book-open-reader';

document.getElementById('button').addEventListener('click', function (event){
    const storyTitle = storyTitleEl.value;
    const childName = childNameEl.value;
    const appearance = appearanceEl.value;
    const storyAbout = storyAboutEl.value;
    const specialEmphasis = specialEmphasisEl.value;

    event.preventDefault();
    if (!childName || !storyAbout) {
        warnUserForElement([childNameEl, storyAboutEl]);
        return;
    }

    const urlQuery =
        `?name=${childName}&appearance=${appearance}&story-about=${storyAbout}
                &special-emphasis=${specialEmphasis}&title=${storyTitle}`;



    const url = baseGenerateFromQuestionaryUrl + urlQuery;

    clearMainElement();
    createLoadingPage();

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayResult(data['title'], data['slug']);
            console.log(data);
        })
        .catch(error => {
            console.log('Something went wrong', error);
        });
});

function warnUserForElement(elements) {
    elements.map((element) => {
        if (!element.value) {
            element.classList.add('warning');
            setTimeout(() => element.classList.remove('warning'), 3000);
        }
    });

}


function clearMainElement() {
    mainEl.innerHTML = '';
}

function createLoadingPage() {
    wrapperEl.classList.add('loader-wrapper');
    mainEl.append(wrapperEl);

    const titleEl = document.createElement('h2');
    titleEl.textContent = 'We are generating your personalized kids story.'
    wrapperEl.append(titleEl);

    const pEl = document.createElement('p');
    pEl.textContent = 'This process might take up to 2 minutes, feel free to leave this page, and find the ready result in ' +
        'your account profile page whenever it is ready.'
    wrapperEl.append(pEl);

    const loaderEl = document.createElement('div');
    loaderEl.classList.add('loader');
    wrapperEl.append(loaderEl);
}

function displayResult(storyName, storySlug) {
    titleEl = document.querySelector('.loader-wrapper > h2:first-of-type');
    titleEl.textContent = 'Yey... Your personalized story has been generated';

    const loader = document.querySelector('.loader');
    loader.remove();

    const pEl = document.querySelector('.loader-wrapper > p:first-of-type');
    pEl.remove();

    const h3El = document.createElement('h3');
    h3El.textContent = storyName;
    wrapperEl.append(h3El);

    const newPEl = document.createElement('p');
    newPEl.textContent = 'Thank you for generating a unique story with Tiny Tale Factory. You can view your' +
        'story directly by clicking the bellow button, or you can find it in your account page.';
    wrapperEl.append(newPEl);

    const viewStoryLinkEl = document.createElement('a');
    viewStoryLinkEl.classList.add('view-story-btn');
    viewStoryLinkEl.textContent = 'View Story';
    viewStoryLinkEl.setAttribute('href', baseViewStoryUrl.replace('placeholder', storySlug));
    wrapperEl.append(viewStoryLinkEl);

    const iEl = document.createElement('i');
    iEl.className = bookOpenReaderClass;
    viewStoryLinkEl.append(iEl);
}
