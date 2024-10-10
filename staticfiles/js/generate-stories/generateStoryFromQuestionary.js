const mainEl = document.querySelector('.header-container');
const storyTitleEl = document.getElementById('title');
const childNameEl = document.getElementById('name');
const appearanceEl = document.getElementById('appearance');
const storyAboutEl = document.getElementById('about');
const specialEmphasisEl = document.getElementById('special-emphasis');

const bookOpenReaderClass = 'fa-solid fa-book-open-reader';
let a = createLoadingPage;
document.getElementById('button').addEventListener('click', function (event){
    event.preventDefault();

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

    clearMainElement(mainEl);
    const wrapperEl = createLoadingPage();
    mainEl.append(wrapperEl);

    fetch(url)
        .then(response => {
            if (response.status === 401) {
                unauthorizedAccess(wrapperEl);
                throw new Error('Unauthorized access to API.');
            }
        })

        .then(data => {
            displayResult(data['title'], data['slug'], wrapperEl);
        })

        .catch(error => {
            console.error('Something went wrong', error);
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
