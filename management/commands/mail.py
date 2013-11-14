#-*- coding: utf-8 -*-

from datetime import datetime, timedelta

from pytz import timezone

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from when.models import *

tzloc = timezone(settings.TIME_ZONE).localize


class Command(BaseCommand):
    args = u''
    help = u'Donne le champ TO si on veut envoyer un mail à tout le monde'

    def handle(self, *args, **options):
        liste = [u'%s %s <%s>' % (u.first_name, u.last_name, u.email) for u in User.objects.annotate(num_groups=Count('groupe')).filter(num_groups__gt=0)]
        self.stdout.write(', '.join(liste))
