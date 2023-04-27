from datetime import datetime, timedelta
import json

from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, reverse
from django.views.decorators.csrf import csrf_exempt

import jwt
import requests
import webbrowser

def get_payload(user, preferred_region, preferred_provider, amount):
    amount = 9.99
    exp = int((datetime.utcnow() + timedelta(seconds=10*60)).timestamp())
    merchantReference = 'Annetus-' + '-'.join(str(x) for x in datetime.now().timetuple()[:6]) # TODO: Ajutine uuid lahendus
    # 1. Gather the checkout data
    payload = {
        "accessKey": settings.MY_ACCESS_KEY,
        "merchantReference": merchantReference,
        "returnUrl": f"http://test.valgalinn.ee:8000/montonio/naase/{merchantReference}/",
        "notificationUrl": "http://test.valgalinn.ee:8000/montonio/teavita/",
        "currency": "EUR",
        "exp": exp,
        "grandTotal": amount,
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
            "amount": amount,  # Yes, this is the same as order['grandTotal'].
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
        # print(settings.MONTONIO_API_SERVER)

        # 4. Send the token to the API and get the payment URL
        response = requests.post(
            f'{settings.MONTONIO_API_SERVER}/orders',
            json={
                'body': token
            },
            headers={'Content-Type: application/json'}
        )
        data = response.json()
        # payment_url = data['paymentUrl']

        # 5. Redirect the customer to the checkout page
        # return redirect(payment_url)
    else:
        data = 'NOK'
    return JsonResponse({'data': data})

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
    return json.dumps(data)
    # return JsonResponse({'data': data})

def index(request):
    # storeSetupData = get_payment_methods()
    return render(
        request,
        "montonio/index.html",
        {
            'my_access_key': settings.MY_ACCESS_KEY,
            # 'storeSetupData': storeSetupData
        }
    )

@csrf_exempt
def naase(request, merchantReference):
    print('naase', merchantReference, request.method)
    if request and request.method == 'GET':
        print(request.GET)
        # Fetched from the URL for returnUrl and from POST body->orderToken when it's a notification
        # orderToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoidGhlLW1vbnRvbmlvLW9yZGVyLXV1aWQiLCJhY2Nlc3NLZXkiOiJNWV9BQ0NFU1NfS0VZIiwibWVyY2hhbnRSZWZlcmVuY2UiOiJNWS1PUkRFUi1JRC0xMjMiLCJtZXJjaGFudFJlZmVyZW5jZURpc3BsYXkiOiJNWS1PUkRFUi1JRC0xMjMiLCJwYXltZW50U3RhdHVzIjoiUEFJRCIsImdyYW5kVG90YWwiOjk5Ljk5LCJjdXJyZW5jeSI6IkVVUiIsIm1lcmNoYW50X3JlZmVyZW5jZSI6Ik1ZLU9SREVSLUlELTEyMyIsIm1lcmNoYW50X3JlZmVyZW5jZV9kaXNwbGF5IjoiTVktT1JERVItSUQtMTIzIiwicGF5bWVudF9zdGF0dXMiOiJQQUlEIn0.X6Ym70AA1bYIsKyNc1NL4NpznKXCrGX5xacqc1ovtuE'
        orderToken = request.GET.get('order-token')
        # The Order ID you got from Montonio as a response to creating the order
        # montonioOrderId = 'the-montonio-order-uuid'

        try:
            decoded = jwt.decode(
                orderToken,
                settings.MY_SECRET_KEY,
                algorithms=['HS256']
            )
            print(decoded)
        except jwt.exceptions.InvalidSignatureError as identifier:
            pass  # Token validation failed

        if (
                decoded['paymentStatus'] == 'PAID'
                # and decoded['uuid'] == merchantReference
                and decoded['merchantReference'] == merchantReference
                and decoded['accessKey'] == settings.MY_ACCESS_KEY
        ):
            print('PAID')
            pass  # Payment completed
        else:
            print('NOT PAID')
            pass  # Payment not completed
    return redirect(reverse('montonio:index'))

@csrf_exempt
def teavita(request):
    print('teavita', request.method)
    if request:
        print(request.body)
    return redirect(reverse('montonio:index'))
