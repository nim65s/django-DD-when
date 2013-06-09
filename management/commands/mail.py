#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from when.models import Moment, DispoToPlay, Groupe

from datetime import datetime, timedelta
from pytz import timezone

tzloc = timezone(settings.TIME_ZONE).localize

class Command(BaseCommand):
    args = u''
    help = u'Donne le champ TO si on veut envoyer un mail à tout le monde'

    def handle(self, *args, **options):
        self.stdout.write(', '.join([u'%s % <%s>' % (u.first_name, u.last_name, u.email) for u in User.objects.annotate(num_groups=Count('groupe')).filter(num_groups__gt=0)]))
