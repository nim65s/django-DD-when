from datetime import timedelta

from django.template import Library
from django.template.defaultfilters import date
from django.templatetags.tz import utc

register = Library()


@register.filter
def ics_date(value, arg=0):
    """ Formate une date comme il faut pour un ics, avec éventuelement un ajout d’heures """
    if arg:
        value += timedelta(hours=arg)
    value = utc(value)
    return date(value, 'Ymd\THis\Z')
