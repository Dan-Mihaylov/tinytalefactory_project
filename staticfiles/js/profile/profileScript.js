const userInfoListItems = document.querySelectorAll('.user-info-list-items');
const onHoverWrapperElement = document.querySelectorAll('.on-hover-wrapper')[0];
const profileWrapperRight = document.getElementById('profile-wrapper-right');
const changeUserInfoElement = document.getElementById('change-user-info');
const showStoriesElement = document.getElementById('display-stories');
const getTokensButtonElement = document.querySelector('.buy-more');

const emailSettingsEl = document.getElementById('email-settings');
const setPasswordEl = document.getElementById('password');

getTokensButtonElement.addEventListener('click', displayGetTokensDiv);
emailSettingsEl.addEventListener('click', createIframeElement);
setPasswordEl.addEventListener('click', createIframeElement);
setPasswordEl.addEventListener('click', createIframeElement);

showStoriesElement.addEventListener('click', showStories);

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
function fillStoriesCountElement (totalStories){
    const storyCountElement = document.querySelectorAll('.user-info-list-items')[0];
    const spanElement = storyCountElement.children[1];

    function delay (){
        const currNumber = Number(spanElement.textContent);
        spanElement.textContent = currNumber + 1;
        setTimeout(recurse(currNumber + 1), 50);
    }

    function recurse (n){
        if (n === totalStories) {
            return;
        }
        setTimeout(delay, 50);
    }

    recurse(Number(0));
}

// TODO: Create animation for all profile info numbers
function fillTokensCountElements (){
    const spanElements = [...document.querySelectorAll('.user-info-list span')].slice(1);

    const [totalTokensEl, promoTokensEl] = spanElements;
    totalTokensEl.textContent = totalTokens;
    promoTokensEl.textContent = promotionalTokens;
}

function onload (){
    fetch(url)
        .then(response => response.json())
        .then(data => {
            fillStoriesCountElement(data.length);
            fillTokensCountElements();
            data.forEach(story => {
            })
        })
}

onload();

// Create iframe Element
function createIframeElement (event){

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

function addStylesheetToPasswordFrameDocument (){
    const frameElement = document.getElementById('set-password-frame');

    const contentDocument = frameElement.contentDocument;
    const activeBodyElement = contentDocument.activeElement;

    const availableButtons = activeBodyElement.querySelectorAll('form button');

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


function addStylesheetToEmailFrameDocument (){

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

function displayChangeUserInfoDiv (event){
    clearProfileWrapperRight();
    clearChildrenSelectedClass(event.target.parentNode);
    event.target.classList.add('selected');


    // create a new wrapper
    const wrapperElement = createNewRightWrapper();

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

function createNewRightWrapper (){
    const wrapperElement = document.createElement('div');
    wrapperElement.style.tranition = 'opacity 1s linear';
    wrapperElement.style.opacity = '0';
    wrapperElement.classList.add('right-info-wrapper');
    profileWrapperRight.append(wrapperElement);
    setTimeout(() => wrapperElement.style.opacity = '100', 10);

    return wrapperElement;
}

function fillKnownProfileInfo (usernameElement, firstNameElement, lastNameElement){
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

function submitNewProfileInfo (event){
    event.preventDefault();

    const rightInfoWrapperElement = document.querySelectorAll('.right-info-wrapper')[0];
    const url = '/api/users/';
    const userInfo = {
        'username': document.getElementById('username-input').value,
        'first_name': document.getElementById('first-name-input').value,
        'last_name': document.getElementById('last-name-input').value
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
        .catch(error => console.error('Error with edit data: ', error));

    function createSuccessElement (){

        const paragraphElement = document.createElement('p');
        paragraphElement.classList.add('success-warning');
        paragraphElement.style['opacity'] = 0;
        paragraphElement.textContent = 'Your details have been successfully changed!'
        return paragraphElement;
    }

    function addElementToWrapper (element){
        rightInfoWrapperElement.append(element);
        element.style.opacity = 1;

        setTimeout(() => {
            element.style.opacity = 0;
            setTimeout(() => {
                rightInfoWrapperElement.removeChild(element)
            }, 1)
        }, 10000)
    }
}

function clearProfileWrapperRight (){
    profileWrapperRight.innerHTML = '';
}

function clearChildrenSelectedClass (node){
    [...node.children].map(child => {
        child.classList.remove('selected');
    });
}

// Display buy more tokens wrapper
function displayGetTokensDiv (event){
    const infoTextContent = '' +
        'The price per token is £1.20. One token generates one children story, which you can download\n'
        + 'as many times as you wish. Currently, we support only <strong>PayPal</strong> as a means of payment.\n'
        + 'You can get 30% off from your purchase by buying 6 or more tokens. For full terms and conditions\n'
        + 'please read <a id="terms-and-conditions" href="#">T&C\'s</a>'

    clearProfileWrapperRight();

    // create new right wrapper el
    const wrapperElement = createNewRightWrapper();

    // create wrapper overlay for loader
    const overlayEl = document.createElement('div');
    overlayEl.classList.add('loader-overlay');
    overlayEl.style.display = 'none';
    wrapperElement.append(overlayEl);

    const loadingPEl = document.createElement('p');
    loadingPEl.textContent = 'Processing';
    overlayEl.append(loadingPEl);

    const loaderEl = document.createElement('div');
    loaderEl.classList.add('loader');
    overlayEl.append(loaderEl);

    // create header el
    const headerEl = document.createElement('h2');
    headerEl.textContent = 'Buy More Tokens';
    wrapperElement.append(headerEl);

    // create form element
    const formEl = document.createElement('form');
    formEl.classList.add('token-buy-form');
    wrapperElement.append(formEl);

    // First field
    const firstFieldEl = document.createElement('div');
    firstFieldEl.classList.add('tokens-form-field');
    formEl.append(firstFieldEl);

    const firstLabelEl = document.createElement('label');
    firstLabelEl.setAttribute('for', 'tokens-amount');
    firstFieldEl.textContent = 'Tokens: ';
    firstFieldEl.append(firstLabelEl);

    const tokensBuyContainerEl = document.createElement('div');
    tokensBuyContainerEl.classList.add('tokens-buy-container');
    firstFieldEl.append(tokensBuyContainerEl);

    const minusSpanEl = document.createElement('span');
    minusSpanEl.setAttribute('id', 'minus-token');
    minusSpanEl.addEventListener('click', minusToken);

    const minusIElement = document.createElement('i');
    minusIElement.className = 'fa-solid fa-minus';
    minusSpanEl.append(minusIElement);

    tokensBuyContainerEl.append(minusSpanEl);

    const tokenAmountInputEl = document.createElement('input');
    tokenAmountInputEl.setAttribute('type', 'number');
    tokenAmountInputEl.setAttribute('min', 0);
    tokenAmountInputEl.setAttribute('id', 'tokens-amount');
    tokenAmountInputEl.setAttribute('name', 'tokens-amount');
    tokenAmountInputEl.value = '0';
    tokensBuyContainerEl.append(tokenAmountInputEl);

    const plusSpanEl = document.createElement('span');
    plusSpanEl.setAttribute('id', 'plus-token');
    plusSpanEl.addEventListener('click', plusToken);

    const plusIElement = document.createElement('i');
    plusIElement.className = 'fa-solid fa-plus';
    plusSpanEl.append(plusIElement);

    tokensBuyContainerEl.append(plusSpanEl)

    // Second field
    const secondFieldEl = document.createElement('div');
    secondFieldEl.classList.add('tokens-form-field');
    formEl.append(secondFieldEl);

    const secondLabelEl = document.createElement('label');
    secondLabelEl.setAttribute('for', 'tokens-price');
    secondLabelEl.textContent = 'Total price:';
    secondFieldEl.append(secondLabelEl);

    const priceInputEl = document.createElement('input');
    priceInputEl.setAttribute('type', 'text');
    priceInputEl.setAttribute('id', 'tokens-price');
    priceInputEl.setAttribute('disabled', 'disabled');
    priceInputEl.value = '£0.00';
    secondFieldEl.append(priceInputEl);

    // buy tokens info element
    const smallInfoEl = document.createElement('small');
    smallInfoEl.classList.add('buy-tokens-info');
    smallInfoEl.innerHTML = infoTextContent;
    wrapperElement.append(smallInfoEl);

    // Paypal button container
    const paypalContainerEl = document.createElement('div');
    paypalContainerEl.setAttribute('id', 'paypal-button-container');
    wrapperElement.append(paypalContainerEl);

    const paypalBtnEl = document.createElement('a');
    paypalBtnEl.setAttribute('id', 'paypal-btn');

    paypalBtnEl.textContent = "Create order";
    paypalContainerEl.append(paypalBtnEl);

    const cartEl = document.createElement('i');
    cartEl.className = "fa-solid fa-cart-plus";
    paypalBtnEl.appendChild(cartEl);

    // Order created el
    const orderCreatedPEl = document.createElement('p');
    orderCreatedPEl.classList.add('order-details-info');
    orderCreatedPEl.textContent = 'Order created successfully, please continue to payment';
    orderCreatedPEl.style.display = 'none';
    wrapperElement.append(orderCreatedPEl);

    const termsAndConditionsEl = generateTermsAndConditionsElement();
    wrapperElement.append(termsAndConditionsEl);

    initButton();
    const nodeToClearChildrenTo = document.querySelector('.settings-options-wrapper').children[0]
    clearChildrenSelectedClass(nodeToClearChildrenTo);
}

function generateTermsAndConditionsElement() {
    let text;
    const termsAndCondOverlay = document.createElement('div');
    termsAndCondOverlay.classList.add('terms-and-cons-overlay');
    termsAndCondOverlay.style.display = 'none';

    text = 'Terms and Conditions for Tiny Tale Factory';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'Last Updated: 03/09/2024';
    termsAndCondOverlay.append(createContentEl(text));

    text = 'Welcome to Tiny Tale Factory, a platform that generates children\'s stories using OpenAI ' +
        'and DALL-E 3 technologies. By accessing or using our website, you agree to comply with and be bound by these' +
        ' Terms and Conditions. Please read these terms carefully. If you do not agree with any part of these terms, ' +
        'you should not use our website.'
    termsAndCondOverlay.append(createContentEl(text));

    text = '1. Services Provided';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'Tiny Tale Factory provides an online platform for generating children\'s stories' +
        ' using OpenAI and DALL-E 3. These stories are generated based on user input and preferences. We do not ' +
        'moderate or control the content generated by DALL-E 3 or the text of the stories. The content is' +
        ' generated automatically and may vary based on the inputs provided by users.'
    termsAndCondOverlay.append(createContentEl(text));

    text = '2. User Responsibility';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'By using our services, you confirm that you are at least 18 years of age or have parental consent ' +
        'to use this website. You agree to use the services provided for lawful purposes only. You must not use' +
        ' our website in any way that causes, or may cause, damage to the website or impairment of the availability ' +
        'or accessibility of the website.'
    termsAndCondOverlay.append(createContentEl(text));

    text = 'Intellectual Property';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'All content generated on this website, including but not limited to text, graphics, images, and software,' +
        ' is the property of [Your Website Name] and is protected by copyright, trademark, and other intellectual ' +
        'property laws. You may not reproduce, distribute, or use any content without our express written permission.';
    termsAndCondOverlay.append(createContentEl(text));

    text = '4. Payment and Billing';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'We use PayPal as our payment method. By using our services, you agree to the payment terms set ' +
        'forth by PayPal. You are responsible for ensuring that all payment information provided is accurate ' +
        'and complete. All payments must be successfully completed before accessing the generated content.';
    termsAndCondOverlay.append(createContentEl(text));

    text = '4.1 Promotional Offer';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'We are currently offering a 30% discount if you purchase 5 or more tokens. This offer is subject ' +
        'to availability and may be withdrawn at any time without notice. Tiny Tale Factory reserves the right to' +
        ' modify or terminate promotional offers at its discretion.';
    termsAndCondOverlay.append(createContentEl(text));

    text = '5. Refund Policy';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'Due to the digital nature of our services, all sales are final. We do not offer refunds once the story ' +
        'generation process has started, unless there is a technical issue on our end that prevents the delivery ' +
        'of the content.';
    termsAndCondOverlay.append(createContentEl(text));

    text = '6. Disclaimer of Warranties'
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'Tiny Tale Factory provides the services "as is" and "as available." We make no representations or ' +
        'warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, ' +
        'or availability with respect to the website or the information, products, services, or related graphics' +
        ' contained on the website for any purpose. Any reliance you place on such information is therefore ' +
        'strictly at your own risk.';
    termsAndCondOverlay.append(createContentEl(text));

    text = '7. Limitation of Liability';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'To the fullest extent permitted by law, Tiny Tale Factory shall not be liable for any indirect,' +
        ' incidental, special, consequential, or punitive damages, or any loss of profits or revenues, ' +
        'whether incurred directly or indirectly, or any loss of data, use, goodwill, or other intangible losses,' +
        ' resulting from (i) your use or inability to use the services; (ii) any unauthorized access to or use of' +
        ' our servers and/or any personal information stored therein.';
    termsAndCondOverlay.append(createContentEl(text));

    text = '8. Indemnification';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'You agree to indemnify, defend, and hold harmless Tiny Tale Factory, its officers, employees, ' +
        'and agents from any claims, liabilities, damages, losses, and expenses, including, without limitation,' +
        ' reasonable legal and accounting fees, arising out of or in any way connected with your access to or use ' +
        'of our services or your violation of these Terms.';
    termsAndCondOverlay.append(createContentEl(text));

    text = '9. Data Privacy';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'We respect your privacy and are committed to protecting your personal information. ' +
        'We do not store any personal information other than the order ID and the status of the payment ' +
        '(whether it has been successfully paid or not). The only cookies we use are those necessary for the proper ' +
        'functioning of the site, such as session management and payment processing.' +
        ' Please note that this policy may change, and additional cookies may be used in the future to' +
        'improve user experience or for other purposes. Any changes to our cookie usage will be reflected in an ' +
        'updated version of our Privacy Policy.';
    termsAndCondOverlay.append(createContentEl(text));

    text = '10. Modifications to the Terms';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'Tiny Tale Factory reserves the right to modify these Terms and Conditions at any time. ' +
        'We will notify you of any changes by posting the new Terms on this page. Your continued use of the' +
        ' website after any such changes constitutes your acceptance of the new Terms.';
    termsAndCondOverlay.append(createContentEl(text))

    text = '11. Governing Law';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'These Terms and Conditions are governed by and construed in accordance with the laws of the United Kingdom.' +
        ' Any disputes relating to these terms will be subject to the exclusive jurisdiction of the courts of the UK.';
    termsAndCondOverlay.append(createContentEl(text));

    text = '12. Contact Information';
    termsAndCondOverlay.append(createHeaderEl(text));

    text = 'If you have any questions about these Terms and Conditions, please contact us.';
    termsAndCondOverlay.append(createContentEl(text));

    // TODO: change contact us link
    const contactUsEl = document.createElement('a');
    contactUsEl.setAttribute('href', '#');
    contactUsEl.textContent = 'Get in touch';
    termsAndCondOverlay.append(contactUsEl);

    return termsAndCondOverlay;

}

function createHeaderEl (text) {
    const headerEl = document.createElement('h3');
    headerEl.textContent = text;
    return headerEl;
}

function createContentEl (text) {
    const contentEl = document.createElement('p');
    contentEl.textContent = text;
    return contentEl;
}

// Show stories button functionality
async function showStories (event){
    try {
        clearChildrenSelectedClass(event.target.parentNode);
        event.target.classList.add('selected');
        const stories = await getStories();
        const storyElements = createStoryCards(stories);
        displayStoryElements(storyElements);
    } catch (error) {
        console.error(error);
    }
}

async function getStories (){

    try {
        const response = await fetch(getStoriesURL);
        const responseJson = await response.json();
        const responseValues = Array.from(Object.values(responseJson));
        return responseValues;
    } catch (error) {
        console.error(error);
    }

}

function createStoryCards (storiesArray){
    const generatedElements = [];
    const fontAwesomeBookClass = 'fa-solid fa-book-open-reader';

    storiesArray.forEach(story => {
        const storySlug = story['slug'];
        const storyTitle = story['title'];
        const storyImage = story['info']['urls'][0];
        const createdAt = story['created_at'].split('T')[0].replaceAll('-', '/');
        const storyUrl = baseStoryViewUrl.replace('placeholder', storySlug);

        // Card Element Creation
        const storyCardEl = document.createElement('div');
        storyCardEl.classList.add('story-card');

        // Left - Media side
        const storyMediaEl = document.createElement('div');
        storyMediaEl.classList.add('story-media');
        storyCardEl.append(storyMediaEl);

        const imgEl = document.createElement('img');
        imgEl.setAttribute('src', storyImage);
        storyMediaEl.append(imgEl);

        // Right - Article side
        const articleEl = document.createElement('article');
        articleEl.classList.add('story-info-article');
        storyCardEl.append(articleEl);

        const titleEl = document.createElement('h3');
        titleEl.textContent = storyTitle;
        articleEl.append(titleEl);

        const createdOnEl = document.createElement('p');
        createdOnEl.textContent = 'Created On: ';
        articleEl.append(createdOnEl);

        const dateEl = document.createElement('date');
        dateEl.textContent = createdAt;
        createdOnEl.append(dateEl);

        const linkEl = document.createElement('a');
        linkEl.textContent = 'View story';
        linkEl.setAttribute('href', storyUrl);
        articleEl.append(linkEl);

        const bookEl = document.createElement('i');
        bookEl.className = fontAwesomeBookClass;
        articleEl.append(bookEl);

        generatedElements.push(storyCardEl);
    });

    return generatedElements;
}

function displayStoryElements (storiesArray){
    clearProfileWrapperRight();

    const storiesWrapperEl = document.createElement('div');
    storiesWrapperEl.classList.add('stories-wrapper');
    storiesWrapperEl.style.opacity = '0';

    const headerEl = document.createElement('h2');
    headerEl.textContent = 'All your generated stories';
    storiesWrapperEl.append(headerEl)

    storiesArray.forEach(storyDiv => storiesWrapperEl.append(storyDiv));

    profileWrapperRight.append(storiesWrapperEl);

    setTimeout(() => storiesWrapperEl.style.opacity = '100', 10);
}

// On first load of page

setTimeout(() => showStories(showStoriesElement.click()), 1000);
