from datetime import datetime, timedelta
import json

from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

import jwt
import requests
import webbrowser

def get_payload(user, preferred_region, preferred_provider, amount):
    exp = int((datetime.utcnow() + timedelta(seconds=10*60)).timestamp())
    # 1. Gather the checkout data
    payload = {
        "accessKey": settings.MY_ACCESS_KEY,
        "merchantReference": "ANNETUS123",
        "returnUrl": "http://test.valgalinn.ee:8000/montonio/naase",
        "notificationUrl": "http://test.valgalinn.ee:8000/montonio/teavita",
        "currency": "EUR",
        "exp": exp,
        "grandTotal": 9.99,
        "locale": "et",
        # "billingAddress": {
        #     "firstName": "Kalev",
        #     "lastName": "Härk",
        #     "email": "kalev.hark@mail.ee",
        #     "addressLine1": "Kai 1",
        #     "locality": "Tallinn",
        #     "region": "Harjumaa",
        #     "country": "EE",
        #     "postalCode": "10111"
        # },
        # "shippingAddress": {
        #     "firstName": "Kalev",
        #     "lastName": "Härk",
        #     "email": "kalev.hark@mail.ee",
        #     "addressLine1": "Kai 1",
        #     "locality": "Tallinn",
        #     "region": "Harjumaa",
        #     "country": "EE",
        #     "postalCode": "10111"
        # },
        # "lineItems": [
        #     {
        #         "name": "Annetus",
        #         "quantity": 1,
        #         "finalPrice": 9.99
        #     }
        # ],

        # 2. Specify the payment method
        "payment": {
            "method": "paymentInitiation",
            "methodDisplay": "Maksa läbi oma panga",
            "methodOptions": {
                "paymentDescription": f"{user} annetus",
                "preferredCountry": preferred_region,
                # This is the code of the bank that the customer chose at checkout.
                # See the GET /stores/payment-methods endpoint for the list of available banks.
                "preferredProvider": preferred_provider
            },
            "amount": 9.99,  # Yes, this is the same as order['grandTotal'].
            "currency": "EUR"  # This must match the currency of the order.
        }
    }
    return payload

def get_order(request):
    if request:
        # 1. Gather the checkout data
        # 2. Specify the payment method
        data = json.loads(request.body)
        user = data['User']
        amount = data['Amount']
        preferred_region = data['Preferred region']
        preferred_provider = data['Preferred provider']

        payload = get_payload(user, preferred_region, preferred_provider, amount)
        # 3. Generate the token
        token = jwt.encode(payload, settings.MY_SECRET_KEY, algorithm='HS256')
        print(settings.MONTONIO_API_SERVER)

        # 4. Send the token to the API and get the payment URL
        response = requests.post(f'{settings.MONTONIO_API_SERVER}/orders', json={
            'body': token
        })
        data = response.json()
        # payment_url = data['paymentUrl']

        # 5. Redirect the customer to the checkout page
        print(data)
        # webbrowser.open(payment_url)
    else:
        data = 'NOK'
    return JsonResponse({'data': data})

def index(request):
    storeSetupData = get_payment_methods()
    return render(
        request,
        "montonio/index.html",
        {
            'my_access_key': settings.MY_ACCESS_KEY,
            'storeSetupData': storeSetupData
        }
    )

def get_payment_methods():
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
        f'{settings.MONTONIO_API_SERVER}/stores/payment-methods',
        headers={'Authorization': f'Bearer {auth_header}'}
    )
    data = response.json()
    print(data)
    # return JsonResponse({'data': data})

def naase(request):
    if request:
        print(request.META)
    return redirect('/')

def teavita(request):
    if request:
        print(request.body)
    get_payment_methods()
    return redirect('/')
