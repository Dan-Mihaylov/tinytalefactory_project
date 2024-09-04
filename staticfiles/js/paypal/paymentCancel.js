async function paymentCancel (){
    try {
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfTokenValue,
            },
            body: JSON.stringify({'order_id': orderId})
        };

        const response = await fetch(paymentCancelUrl, options);
        const responseData = await response.json();

        console.log(responseData);

    } catch (error) {
        console.error(error);
    }
}

paymentCancel();
