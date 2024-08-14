const userInfoListItems = document.querySelectorAll('.user-info-list-items');
const onHoverWrapperElement = document.querySelectorAll('.on-hover-wrapper')[0];
const profileWrapperRight = document.getElementById('profile-wrapper-right');
const changeUserInfoElement = document.getElementById('change-user-info');

const emailSettingsEl = document.getElementById('email-settings');
const setPasswordEl = document.getElementById('password');



emailSettingsEl.addEventListener('click', createIframeElement);
setPasswordEl.addEventListener('click', createIframeElement);
setPasswordEl.addEventListener('click', createIframeElement);

// Display help text on icon hover
Array.from(userInfoListItems)
    .forEach(el => {
        el.addEventListener('mouseenter', (event) => {
            const newTextContent = event.target.querySelector('p').textContent;
            const pElement = onHoverWrapperElement.children[0];
            pElement.textContent = newTextContent;
            pElement.style.opacity = '100';
        });
        el.addEventListener('mouseleave', (event) => {
            const pElement = onHoverWrapperElement.children[0];
            pElement.style.opacity = '0';
        })
    })

// Animation fill stories counter
function fillStoriesCountElement(totalStories) {
    const storyCountElement = document.querySelectorAll('.user-info-list-items')[0];
    const spanElement = storyCountElement.children[1];

    function delay() {
        const currNumber = Number(spanElement.textContent);
        spanElement.textContent = currNumber + 1;
        setTimeout(recurse(currNumber + 1), 50);
    }

    function recurse(n) {
        if (n == totalStories) {
            return;
        }
        setTimeout(delay, 50);
    }

    recurse(Number(0));
}

function onload() {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            fillStoriesCountElement(data.length);
            data.forEach(story => {
            })
        })
}

onload();

// Create iframe Element
function createIframeElement(event) {

    clearChildrenSelectedClass(event.target.parentNode);
    event.target.classList.add('selected');
    clearProfileWrapperRight();

    const targetId = event.target.getAttribute('id');
    const iFrameEl = document.createElement('iframe');

    switch (targetId) {
        case 'email-settings':
            iFrameEl.setAttribute('id', 'change-email-frame');
            iFrameEl.setAttribute('src', accountEmailUrl);
            iFrameEl.setAttribute('title', 'Account Email Settings');

            profileWrapperRight.append(iFrameEl);

            setTimeout(addStylesheetToEmailFrameDocument, 300);
            break;

        case 'password':
            iFrameEl.setAttribute('id', 'set-password-frame');
            iFrameEl.setAttribute('src', accountSetPasswordSetUrl);
            iFrameEl.setAttribute('title', 'Account Set Password');

            profileWrapperRight.append(iFrameEl);

            setTimeout(addStylesheetToPasswordFrameDocument, 300);
            break;
    }

}

// Change email iFrame TODO: Maybe a different approach

function addStylesheetToPasswordFrameDocument() {
    console.log('PASSWORD SET');
    const frameElement = document.getElementById('set-password-frame');

    const contentDocument = frameElement.contentDocument;
    const activeBodyElement = contentDocument.activeElement;

    const availableButtons = activeBodyElement.querySelectorAll('form button');
    console.log(availableButtons);
    availableButtons.forEach(button => {
        button.addEventListener('click', () => {
            frameElement.style.opacity = '0';
            setTimeout(addStylesheetToPasswordFrameDocument, 1500);
        })
    });

    // include the nested-allauth.css as a style so it can be displayed appropriately
    const linkEl = document.createElement('link');
    linkEl.setAttribute('rel', 'stylesheet');
    linkEl.setAttribute('href', nestedStyleUrl);

    contentDocument.head.appendChild(linkEl);

    // change opacity to 1
    frameElement.style.opacity = '100';

}


function addStylesheetToEmailFrameDocument() {
    console.log('entered!')
    const frameElement = document.getElementById('change-email-frame');

    const contentDocument = frameElement.contentDocument;
    const activeBodyElement = contentDocument.activeElement;

    const availableButtons = activeBodyElement.querySelectorAll('button');
    availableButtons.forEach(button => {
        button.addEventListener('click', () => {
            frameElement.style.opacity = '0';
            setTimeout(addStylesheetToEmailFrameDocument, 1500);
        });
    });

    // include the nested-allauth.css as a style so it can be displayed appropriately
    const linkEl = document.createElement('link');
    linkEl.setAttribute('rel', 'stylesheet');
    linkEl.setAttribute('href', nestedStyleUrl);

    contentDocument.head.appendChild(linkEl);

    // change opacity to 1
    frameElement.style.opacity = '100';
}

// Change user info functionality
changeUserInfoElement.addEventListener('click', displayChangeUserInfoDiv);

function displayChangeUserInfoDiv(event) {
    clearProfileWrapperRight();
    clearChildrenSelectedClass(event.target.parentNode);
    event.target.classList.add('selected');


    // create a new wrapper
    const wrapperElement = document.createElement('div');
    wrapperElement.classList.add('right-info-wrapper');
    profileWrapperRight.append(wrapperElement);

    // create the header
    const headerElement = document.createElement('h2');
    headerElement.textContent = 'View or Change Your Profile Information';
    wrapperElement.append(headerElement);

    // create a new form
    const formElement = document.createElement('form');
    formElement.classList.add('change-user-info-form');
    wrapperElement.append(formElement);

    // add CSRF_token
    formElement.innerHTML = CSRFToken;

    // create username field
    const usernameFieldDiv = document.createElement('div');
    usernameFieldDiv.classList.add('user-info-form-field');

    const usernameLabelElement = document.createElement('label');
    usernameLabelElement.setAttribute('for', 'username-input');
    usernameLabelElement.textContent = 'Your Username:';

    const usernameInputElement = document.createElement('input');
    usernameInputElement.setAttribute('type', 'text');
    usernameInputElement.setAttribute('placeholder', 'Username');
    usernameInputElement.setAttribute('id', 'username-input');

    usernameFieldDiv.append(usernameLabelElement, usernameInputElement)
    formElement.append(usernameFieldDiv);


    // create first name field
    const firstNameFieldDiv = document.createElement('div');
    firstNameFieldDiv.classList.add('user-info-form-field');

    const firstNameLabelElement = document.createElement('label');
    firstNameLabelElement.setAttribute('for', 'first-name-input');
    firstNameLabelElement.textContent = 'Your First Name:';

    const firstNameInputElement = document.createElement('input');
    firstNameInputElement.setAttribute('type', 'text');
    firstNameInputElement.setAttribute('placeholder', 'First Name');
    firstNameInputElement.setAttribute('id', 'first-name-input');

    firstNameFieldDiv.append(firstNameLabelElement, firstNameInputElement);
    formElement.append(firstNameFieldDiv);

    // create last name field
    const lastNameFieldDiv = document.createElement('div');
    lastNameFieldDiv.classList.add('user-info-form-field');

    const lastNameLabelElement = document.createElement('label');
    lastNameLabelElement.setAttribute('for', 'last-name-input');
    lastNameLabelElement.textContent = 'Your Last Name:';

    const lastNameInputElement = document.createElement('input');
    lastNameInputElement.setAttribute('type', 'text');
    lastNameInputElement.setAttribute('placeholder', 'Last Name');
    lastNameInputElement.setAttribute('id', 'last-name-input');

    lastNameFieldDiv.append(lastNameLabelElement, lastNameInputElement);
    formElement.append(lastNameFieldDiv);

    // create submit button field
    const submitButtonFieldDiv = document.createElement('div');
    submitButtonFieldDiv.classList.add('user-info-form-field');

    const buttonChangeProfileInfoElement = document.createElement('button');
    buttonChangeProfileInfoElement.classList.add('btn', 'btn-submit');
    buttonChangeProfileInfoElement.textContent = 'Submit Changes';
    buttonChangeProfileInfoElement.setAttribute('id', 'change-profile-info-button');

    submitButtonFieldDiv.append(buttonChangeProfileInfoElement);

    formElement.append(submitButtonFieldDiv);

    // add event listener to the button
    buttonChangeProfileInfoElement.addEventListener('click', submitNewProfileInfo);

    // fill the form elements if the info is already available
    fillKnownProfileInfo(usernameInputElement, firstNameInputElement, lastNameInputElement);
}

function fillKnownProfileInfo(usernameElement, firstNameElement, lastNameElement) {
    const url = '/api/users/';

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                usernameElement.value = data.username;
                usernameElement.disabled = true;
            }

            firstNameElement.value = data.first_name;
            lastNameElement.value = data.last_name;
        })
        .catch(error => console.log(error));
}

function submitNewProfileInfo(event) {
    event.preventDefault();

    const rightInfoWrapperElement = document.querySelectorAll('.right-info-wrapper')[0];
    const url = '/api/users/';
    const userInfo = {
        'username': document.getElementById('username-input').value,
        'first_name':document.getElementById('first-name-input').value,
        'last_name':document.getElementById('last-name-input').value
    }

    fetch(url, {
        method: 'PATCH',
        body: JSON.stringify(userInfo),
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFTokenValue
        }
    })
        .then(response => response.json())
        .then(data => {
            const successElement = createSuccessElement();
            addElementToWrapper(successElement);
        })
        .catch(error => console.log('Error with edit data: ', error));

    function createSuccessElement() {

        const paragraphElement = document.createElement('p');
        paragraphElement.classList.add('success-warning');
        paragraphElement.style['opacity'] = 0;
        paragraphElement.textContent = 'Your details have been successfully changed!'
        return paragraphElement;
    }

    function addElementToWrapper(element) {
        rightInfoWrapperElement.append(element);
        element.style.opacity = 1;

        setTimeout(()=>{
            element.style.opacity = 0;
            setTimeout(() => {rightInfoWrapperElement.removeChild(element)}, 1)
        }, 10000)
    }



}

function clearProfileWrapperRight(){
    profileWrapperRight.innerHTML = '';
}

function clearChildrenSelectedClass(node) {
    [...node.children].map(child=>{
        child.classList.remove('selected');
    });
}
