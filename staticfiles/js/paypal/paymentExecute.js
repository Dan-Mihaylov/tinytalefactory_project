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

    } catch (error) {
        console.error(error);
    }
}

if (orderId) {
    paymentExecute();
}
