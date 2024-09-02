import requests
import os
import random
from ..paypal.models import Order

AUTH_URL = 'https://api.sandbox.paypal.com/v1/oauth2/token'
CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')


def get_access_token():
    headers = {
        'Accept': 'application/json',
    }
    data = {
        'grant_type': 'client_credentials',
    }
    response = requests.post(AUTH_URL, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))

    return response.json()['access_token']


def create_reference_number():
    BASE = 'ttf'
    count = Order.objects.count()
    for _ in range(6):
        count *= 10
        count += random.randint(1, 9)
    return BASE + str(count)
