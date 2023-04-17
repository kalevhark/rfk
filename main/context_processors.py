from django.conf import settings

def get_cookie_consent_inuse(request):
    CookieOK = request.COOKIES.get('CookieOK')
    return {
        'COOKIE_CONSENT_INUSE': settings.COOKIE_CONSENT_INUSE,
        'CookieOK': CookieOK
    }
