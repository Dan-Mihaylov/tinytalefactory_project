function createLoadingPage() {
    const wrapperEl = document.createElement('div');
    wrapperEl.classList.add('loader-wrapper');

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

    return wrapperEl;
}


function displayResult(storyName, storySlug, wrapperEl) {
    const titleEl = document.querySelector('.loader-wrapper > h2:first-of-type');
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
