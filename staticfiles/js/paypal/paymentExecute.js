const articleEl = document.getElementById('article-element')
profileUrl = '/profile/';

async function paymentExecute (){
    try {
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfTokenValue,
            },
            body: JSON.stringify({'order_id': orderId})
        };

        const response = await fetch(paymentExecuteUrl, options);

        if (response.status === 200) {
            createSuccessMessage();
            return;
        }

        createErrorMessage();
        return;

    } catch (error) {
        console.error(error);
    }
}

if (orderId) {
    paymentExecute();
}

function createSuccessMessage() {
    articleEl.innerHTML = `<h2>Thank you for your purchase</h2>
                <p>
                    Your order with order id:
                    <br>
                    <strong class="bold">${orderId}</strong>
                    <br>
                    has been successful.
                    <br>
                    It might take up a minute for your account to be credited the bough tokens.
                </p>
                <p>
                    You can now create more exciting stories using our platform.
                    Go to your <a href=${profileUrl}>profile page</a> to view your total tokens.
                </p>`
}

function createErrorMessage() {
    articleEl.innerHTML = `<h2>Oh, no!</h2>
                <p>
                    There is nothing to see here. Go <a href="#" onclick="history.back()">back</a>.
                </p>`
}
