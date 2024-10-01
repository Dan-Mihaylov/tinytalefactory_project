import requests
import os


AUTH_URL = 'https://api.sandbox.paypal.com/v1/oauth2/token'
CREATE_ORDER_URL = 'https://api-m.sandbox.paypal.com/v2/checkout/orders'


CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID', None)
CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET', None)


def get_access_token():
    headers = {
        'Accept': 'application/json',
    }
    data = {
        'grant_type': 'client_credentials',
    }
    response = requests.post(AUTH_URL, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    print(response)
    return response.json()['access_token']


def create_order():
    auth_token = get_access_token()

    headers = {
        'Content-Type': 'application/json',
        'PayPal-Request-Id': 'tinytalefactory001',
        'Authorization': f'Bearer {auth_token}',
    }

    data = '{ "intent": "CAPTURE", "purchase_units": [ { "reference_id": "tinytalefactory001", "amount": { "currency_code": "GBP", "value": "12.00" } } ], "payment_source": { "paypal": { "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "brand_name": "Tiny Tale Factory", "locale": "en-UK", "landing_page": "LOGIN", "user_action": "PAY_NOW", "return_url": "https://127.0.0.1:8000", "cancel_url": "https://127.0.0.1:8000/profile" } } } }'

    response = requests.post(CREATE_ORDER_URL, headers=headers, data=data)
    print(response.json())


def capture_payment(p_id):
    auth_token = get_access_token()
    headers = {
        'Content-Type': 'application/json',
        'PayPal-Request-Id': 'tinytalefactory001',
        'Authorization': f'Bearer {auth_token}',
    }

    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{p_id}/capture',
                             headers=headers)
    print(response.json())


def show_order_details(order_id):
    auth_token = get_access_token()

    headers = {
        'Authorization': f'Bearer {auth_token}',
    }

    response = requests.get(f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}', headers=headers)
    print(response.json())


create_order()
# capture_payment('1FW87496WS607423V')


