let tokensAmountEl;
let minusTokenEl;
let plusTokenEl;
let tokensPriceEl;
let termsAndConsShowEl;
let termsAndConsOverlay;

const price = 1.2;
const discountMultiplier = 0.7;
const discountQualifier = 6;


function initButton (){
    const payBtn = document.getElementById('paypal-btn');
    payBtn.addEventListener('click', startPayment);

    tokensAmountEl = document.getElementById('tokens-amount');
    tokensAmountEl.addEventListener('change', changePriceDisplay);

    tokensPriceEl = document.getElementById('tokens-price')

    minusTokenEl = document.getElementById('minus-token');
    plusTokenEl = document.getElementById('plus-token');

    minusTokenEl.addEventListener('click', minusToken);
    plusTokenEl.addEventListener('click', plusToken);

    termsAndConsShowEl = document.getElementById('terms-and-conditions');
    termsAndConsShowEl.addEventListener('click', toggleTermsAndConditions);

    termsAndConsOverlay = document.querySelector('.terms-and-cons-overlay');

}

function minusToken (event){
    const currValue = Number(tokensAmountEl.value);
    const result = currValue - 1;

    result >= 0 ? tokensAmountEl.value = result : tokensAmountEl.value = 0;
    changePriceDisplay();
}

function plusToken (event){
    const currValue = Number(tokensAmountEl.value);
    tokensAmountEl.value = currValue + 1;
    changePriceDisplay();
}

function changePriceDisplay(event) {
    const tokens = Number(tokensAmountEl.value);
    const currPrice = tokens * price;
    const totalPrice = tokens >= discountQualifier ? currPrice * discountMultiplier : currPrice
    tokensPriceEl.value = `£${totalPrice.toFixed(2)}`;
}

function getQuantity (){
    return Number(tokensAmountEl.value);
}

async function startPayment (){
    const quantity = getQuantity();


    if (!quantity) {
        return;
    }

    toggleOverlay();
    disableInputs();
    removeMinusPlusButtons();

    const data = {'quantity': quantity}
    const options = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFTokenValue,
        }
    }
    try {
        const response = await fetch(startPaymentUrl, options);
        const responseData = await response.json();
        const responseObj = JSON.parse(responseData)

        const href = responseObj.link;

        createPayOrderButton(href);
        toggleOverlay();
        displayOrderCreated();

    } catch (error) {
        console.log(error);
        somethingWentWrong();
    }
}

function createPayOrderButton (href){
    const container = document.querySelector('#paypal-button-container');
    container.innerHTML = '';

    const payButton = document.createElement('a');
    payButton.textContent = 'Continue to payment';
    payButton.style.backgroundColor = 'gold';
    payButton.onmouseover = () => payButton.style.backgroundColor = 'steelblue';
    payButton.onmouseleave = () => payButton.style.backgroundColor = 'gold';
    payButton.setAttribute('id', 'paypal-btn');
    payButton.setAttribute('href', href);
    container.append(payButton);

    const paypalEl = document.createElement('i');
    paypalEl.className = 'fa-brands fa-paypal';
    payButton.append(paypalEl);
}

function somethingWentWrong() {
    const loaderOverlayEl = document.querySelector('.loader-overlay');
    loaderOverlayEl.innerHTML = '';

    const errorEl = document.createElement('h3');
    errorEl.textContent = 'Something went wrong, try again later.';
    loaderOverlayEl.append(errorEl);
}

function displayOrderCreated() {
    const orderDetailsEl = document.querySelector('.order-details-info');
    orderDetailsEl.style.display = 'block';
}

function toggleOverlay() {
    const overlayEl = document.querySelector('.loader-overlay');

    overlayEl.style.display === 'none' ? overlayEl.style.display = 'flex' : overlayEl.style.display = 'none';
}

function disableInputs() {
    tokensAmountEl.setAttribute('disabled', 'disabled');
    tokensAmountEl.style.backgroundColor = 'rgb(81, 190, 150, 0.3)';
    tokensPriceEl.style.backgroundColor = 'rgb(81, 190, 150, 0.3)';
}

function removeMinusPlusButtons() {
    minusTokenEl.remove();
    plusTokenEl.remove();
    fixTokensPriceMargin();
}

function fixTokensPriceMargin() {
    tokensPriceEl.style.margin = 0;
}

function toggleTermsAndConditions(event) {
    console.log('CHANGING THE TERMS AND CODITIONS')
    event.preventDefault();

    termsAndConsOverlay.style.display === 'none'
        ?
        termsAndConsOverlay.style.display = 'flex'
        :
        termsAndConsOverlay.style.display = 'none';
}
