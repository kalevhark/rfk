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

FONDID = {
    'studentFund': 'õpilastele',
    'teacherFund': 'õpetajatele'
}

def get_payload(preferred_region, preferred_provider, amount, targetfund, isikukood):
    # Prepare data for payload
    amount = int(amount)
    exp = int((datetime.utcnow() + timedelta(seconds=10*60)).timestamp())
    merchantReference = '-'.join(
        [
            targetfund,
            '-'.join(str(x) for x in datetime.now().timetuple()[:6]), # TODO: Ajutine uuid lahendus
            isikukood
        ]
    )
    paymentDescription = ' '.join(['Annetus stipendiumifondi', FONDID[targetfund], isikukood])

    # 1. Gather the checkout data
    payload = {
        "accessKey": settings.MY_ACCESS_KEY,
        "merchantReference": merchantReference,
        "merchantReferenceDisplay": paymentDescription,
        "returnUrl": f"http://test.valgalinn.ee:8000/montonio/naase/{merchantReference}/",
        "notificationUrl": "http://test.valgalinn.ee:8000/montonio/teavita/",
        "currency": "EUR",
        "exp": exp,
        "grandTotal": amount,
        "locale": "et",
        # "billingAddress": {
        #     "firstName": "Kalev",
        #     "lastName": "Bull",
        #     "email": "nomail@mail.ee",
        #     "addressLine1": "Kai 1",
        #     "locality": "Tallinn",
        #     "region": "Harjumaa",
        #     "country": "EE",
        #     "postalCode": "10111"
        # },
        # "shippingAddress": {
        #     "firstName": "Kalev",
        #     "lastName": "Bull",
        #     "email": "nomail@mail.ee",
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
                "paymentDescription": paymentDescription,
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
        amount = data['Amount']
        targetfund = data['TargetFund']
        isikukood = data['Isikukood']
        preferred_region = data['Preferred region']
        preferred_provider = data['Preferred provider']

        payload = get_payload(preferred_region, preferred_provider, amount, targetfund, isikukood)
        # 3. Generate the token
        token = jwt.encode(payload, settings.MY_SECRET_KEY, algorithm='HS256')

        # 4. Send the token to the API and get the payment URL
        response = requests.post(
            f'{settings.MONTONIO_API_SERVER}/orders',
            json={
                'body': token
            },
            headers={'Content-Type': 'application/json'}
        )
        data = response.json()
        # payment_url = data['paymentUrl']

        # 5. Redirect the customer to the checkout page
        # return redirect(payment_url)
    else:
        data = 'NOK'
    return JsonResponse({'data': data})

# tagastab võimalikud maksekanalid
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
    targetFund = request.GET.get('targetFund')
    if targetFund and targetFund in FONDID.keys():
        pass
    else:
        targetFund = list(FONDID.keys())[0]
    # storeSetupData = get_payment_methods()
    return render(
        request,
        "montonio/index.html",
        {
            'my_access_key': settings.MY_ACCESS_KEY,
            'targetFund': targetFund,
            # 'storeSetupData': storeSetupData
        }
    )

@csrf_exempt
def naase(request, merchantReference):
    if request and request.method == 'GET':
        # Fetched from the URL for returnUrl and from POST body->orderToken when it's a notification
        orderToken = request.GET.get('order-token')
        # The Order ID you got from Montonio as a response to creating the order
        # montonioOrderId = 'the-montonio-order-uuid'

        try:
            decoded = jwt.decode(
                orderToken,
                settings.MY_SECRET_KEY,
                algorithms=['HS256']
            )
        except jwt.exceptions.InvalidSignatureError as identifier:
            # Token validation failed
            return redirect(reverse('montonio:index'))

        if (
                decoded['paymentStatus'] == 'PAID'
                # and decoded['uuid'] == montonioOrderId
                and decoded['merchantReference'] == merchantReference
                and decoded['accessKey'] == settings.MY_ACCESS_KEY
        ):
            print('PAID')
            message = 'Makse õnnestus'
            pass  # Payment completed
        else:
            print('NOT PAID')
            message = 'Makse jäeti pooleli või ebaõnnestus'
            pass  # Payment not completed
    else: # kui ei ole request.GET
        return redirect(reverse('montonio:index'))

    return render(
        request,
        "montonio/naase.html",
        {
            'decoded': decoded,
            'message': message
        }
    )

@csrf_exempt
def teavita(request):
    print('teavita', request.method)
    if request:
        print(request.body)
    return redirect(reverse('montonio:index'))
