#-*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from when.models import Moment, DispoToPlay, Groupe

from datetime import datetime, timedelta
from pytz import timezone

tzloc = timezone(settings.TIME_ZONE).localize

class Command(BaseCommand):
    args = u'N'
    help = u'Ajoute les dates et des dispos pour les N prochains mois'

    def handle(self, *args, **options):
        N = 1
        if args[0]:
            N = int(args[0])

        now = datetime.now()
        then = now + timedelta(days=N*30)

        end = tzloc(datetime(then.year, then.month, 1, 20))
        jour = timedelta(1)

        for groupe in Groupe.objects.all():
            dt = tzloc(datetime(now.year, now.month, 1, 20))
            jours = [int(i) for i in groupe.jours.split(',')]
            while dt < end:
                if dt.weekday() in jours:
                    moment = Moment.objects.get_or_create(moment=tzloc(datetime(dt.year, dt.month, dt.day, groupe.debut)))
                    if moment[1]:
                        self.stdout.write(u'Création du moment %s' % moment[0])
                        groupe.moments.add(moment[0])
                        groupe.save()
                        self.stdout.write(u'Ajout du moment %s au groupe %s' % (moment[0], groupe))
                    for user in groupe.membres.all():
                        dtp = DispoToPlay.objects.get_or_create(moment=moment[0], user=user)
                        if dtp[1]:
                            self.stdout.write(u'Création de la dispo %s' % dtp[0])
                dt += jour
