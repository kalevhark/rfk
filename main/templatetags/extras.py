# from datetime import date, timedelta

from django import template
from django.conf import settings

from main import views

register = template.Library()

SCORE_CLASSES = ['', 'w3-sand', 'w3-pale-yellow', 'w3-pale-red', 'w3-red']

@register.simple_tag
def get_cookie_consent_inuse():
    return settings.COOKIE_CONSENT_INUSE

@register.filter
def get_value_class(value):
    try:
        return SCORE_CLASSES[int(value)]
    except ValueError:
        return ''

@register.filter
def get_icf_title(value):
    return views.get_rfk_title(value)