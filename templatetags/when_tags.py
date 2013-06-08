#-*- coding: utf-8 -*-

from django.template import Library
from django.templatetags.tz import utc
from django.template.defaultfilters import date

from datetime import timedelta

register = Library()

def ics_date(value, arg=0):
    """ Formate une date comme il faut pour un ics, avec éventuelement un ajout d’heures """
    if arg:
        value += timedelta(hours=arg)
    value = utc(value)
    return date(value, 'Ymd\THis\Z')

register.filter('ics_date', ics_date)
