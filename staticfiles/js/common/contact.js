const formEl = document.querySelector('.contact-us-form');

const emailEl = document.getElementById('email-address');
const queryEl = document.getElementById('contact-query');

const overlayEl = createOverlay();
const loaderEl = createLoader();

const submitBtnEl = document.querySelector('.contact-button');
submitBtnEl.addEventListener('click', submitForm);

async function submitForm(event) {
    event.preventDefault();

    try {
        const body = getElValues();
        if (!body) {
            return;
        }

        displayOverlay();

        const options = {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfTokenValue,
            }
        }

        const response = await fetch(apiContactUrl, options);

        if (response.status === 201) {
            overlayEl.innerHTML = '';
            overlayEl.append(createSuccessMessageWrapper());
        } else {
            overlayEl.innerHTML = '';
            overlayEl.append(createErrorMessageWrapper());
        }



    } catch (error) {
        console.error(error);
    }
}

function displayOverlay() {
    formEl.append(overlayEl);
    setTimeout(()=>overlayEl.style.opacity = 1, 1);
    overlayEl.append(loaderEl);
}

function getElValues() {
    const data = {}
    let flag;

    [emailEl, queryEl].forEach(el=> {
        if (!el.value) {
            markFieldWarning(el);
            flag = true;
        } else {
            data[el.getAttribute('id')] = el.value;
        }
    })

    if (flag) {
        return false;
    }

    if (!validEmail(data['email-address'])) {
        markFieldWarning(emailEl);
        return false;
    }

    return data;
}

function validEmail(email) {
    const pattern = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    const found = email.match(pattern);

    return !!found;
}

function markFieldWarning(field) {
    field.classList.add('warning');
    field.addEventListener('input', ()=> field.classList.remove('warning'));
}

function createOverlay (){
    const overlayEl = document.createElement('div');
    overlayEl.classList.add('contact-form-overlay');
    overlayEl.style.opacity = '0';
    overlayEl.style.transition = 'opacity 0.3s linear';
    return overlayEl
}

function createLoader (){
    const loaderEl = document.createElement('div');
    loaderEl.classList.add('loader');
    return loaderEl
}

function createSuccessMessageWrapper() {
    const wrapperEl = document.createElement('div');
    wrapperEl.classList.add('contact-response-msg-wrapper');

    const headerEl = document.createElement('h3');
    headerEl.textContent = 'Your message has been sent successfully';
    wrapperEl.append(headerEl);

    const pEl = document.createElement('p');
    pEl.textContent = 'Thank you for choosing to contact us, we will review your message and respond as soon as possible.'
    wrapperEl.append(pEl);

    return wrapperEl;
}

function createErrorMessageWrapper() {
    const wrapperEl = document.createElement('div');
    wrapperEl.classList.add('contact-response-msg-wrapper');

    const headerEl = document.createElement('h3');
    headerEl.textContent = 'Something went wrong'
    wrapperEl.append(headerEl);

    const pEl = document.createElement('p');
    pEl.textContent = 'Something went wrong when sending your message. Thank you for your understanding. Please ' +
        'try again later.'
    wrapperEl.append(pEl);

    return wrapperEl;
}
