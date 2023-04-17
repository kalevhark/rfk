# from datetime import date, timedelta

from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_cookie_consent_inuse():
    return settings.COOKIE_CONSENT_INUSE