from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render

import jwt
import requests
import webbrowser

def get_payload():
    # 1. Gather the checkout data
    payload = {
        "accessKey": settings.MY_ACCESS_KEY,
        "merchantReference": "ANNETUS123",
        "returnUrl": "http://test.valgalinn.ee:8000/montonio/naase",
        "notificationUrl": "http://test.valgalinn.ee:8000/montonio/teavita",
        "currency": "EUR",
        "grandTotal": 9.99,
        "locale": "et",
        "billingAddress": {
            "firstName": "Kalev",
            "lastName": "Härk",
            "email": "kalev.hark@mail.ee",
            "addressLine1": "Kai 1",
            "locality": "Tallinn",
            "region": "Harjumaa",
            "country": "EE",
            "postalCode": "10111"
        },
        "shippingAddress": {
            "firstName": "Kalev",
            "lastName": "Härk",
            "email": "kalev.hark@mail.ee",
            "addressLine1": "Kai 1",
            "locality": "Tallinn",
            "region": "Harjumaa",
            "country": "EE",
            "postalCode": "10111"
        },
        "lineItems": [
            {
                "name": "Annetus",
                "quantity": 1,
                "finalPrice": 9.99
            }
        ],

        # 2. Specify the payment method
        "payment": {
            "method": "paymentInitiation",
            "methodDisplay": "Maksa läbi oma panga",
            "methodOptions": {
                "paymentDescription": "Annetus",
                "preferredCountry": "EE",
                # This is the code of the bank that the customer chose at checkout.
                # See the GET /stores/payment-methods endpoint for the list of available banks.
                "preferredProvider": "LHVBEE22"
            },
            "amount": 9.99,  # Yes, this is the same as order['grandTotal'].
            "currency": "EUR"  # This must match the currency of the order.
        }
    }
    return payload

def index(request):
    # 1. Gather the checkout data
    # 2. Specify the payment method
    payload = get_payload()
    # 3. Generate the token
    token = jwt.encode(payload, settings.MY_SECRET_KEY, algorithm='HS256')
    print(settings.MY_SECRET_KEY, settings.MY_ACCESS_KEY, token)

    # 4. Send the token to the API and get the payment URL
    response = requests.post('https://sandbox-stargate.montonio.com/api/orders', json={
        'body': token
    })
    data = response.json()
    # payment_url = data['paymentUrl']

    # 5. Redirect the customer to the checkout page
    print(data)
    # webbrowser.open(payment_url)
    return redirect('/')
    # return render(request, "montonio/index.html", {})

def index_bak(request):
    from datetime import datetime, timedelta
    payload = {
        'accessKey': settings.MY_ACCESS_KEY,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    auth_header = jwt.encode(
        payload,
        settings.MY_SECRET_KEY,
        algorithm='HS256'
    )
    response = requests.get(
        'https://sandbox-stargate.montonio.com/api/stores/payment-methods',
        headers={'Authorization': f'Bearer {auth_header}'}
    )
    data = response.json()
    print(data)
    return redirect('/')

def naase(request):
    if request:
        print(request.META)
    return redirect('/')

def teavita(request):
    if request:
        print(request.META)
    return redirect('/')