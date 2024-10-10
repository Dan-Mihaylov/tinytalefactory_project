const mainEl = document.querySelector('.header-container');

function showDropdown (element) {
    const nameAttribute = element.textContent.trim();
    const dropDown = document.getElementById(nameAttribute);
    const generateButton = document.getElementById(nameAttribute + '-button');

    generateButton.setAttribute('data-protect', 'yes');

    dropDown.style.display === 'none' ? dropDown.style.display = 'block' : siblingsDisplayNone(element);
    generateButton.style.display === 'none' ? generateButton.style.display = 'block' : generateButton.style.display = 'none';
}

function siblingsDisplayNone(element) {

    Array.from(element.parentNode.children).slice(1).forEach(child => {
        if (!child.hasAttribute('data-protect')) {
            child.style.display = 'none';
        }
    });
}

function continueWithStory (element) {
    const formId = element.id.replace('button', 'form');
    const formElement = document.getElementById(formId);

    formElement.style.display === 'none' ? formElement.style.display = 'block' : formElement.style.display = 'none';
}

function generateFromCategory (element) {

    const catName = element.name.toLowerCase().split(' ').join('_');

    const urlQuery = `?category=${catName}`;
    const url = baseGenerateUrl + urlQuery;

    clearMainEl();
    const wrapperEl = createLoadingPage();
    mainEl.append(wrapperEl);
    fetch(url)
        .then(response => {
            if (response.status === 401) {
                unauthorizedAccess(wrapperEl);
                throw new Error('Unauthorized Access');
            }
            response.json();
        })

        .then(data => {
            displayResult(data['title'], data['slug'], wrapperEl);
        })

        .catch(error => console.error('Error:', error));

}


function clearMainEl() {
    mainEl.innerHTML = '';
}
