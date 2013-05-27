#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from when.models import Moment, DispoToPlay, Groupe

from datetime import datetime, timedelta
from pytz import timezone


class Command(BaseCommand):
    args = u''
    help = u'Ajoute les dates et des dispos pour les deux prochains mois'

    def handle(self, *args, **options):
        tz = timezone('Europe/Paris')

        now = datetime.now()
        then = now + timedelta(days=60)

        dt = tz.localize(datetime(now.year, now.month, 1, 20))
        end = tz.localize(datetime(then.year, then.month, 1, 20))

        jour = timedelta(1)
        onze = timedelta(hours=9) # 11h = 20h - 9h

        while dt < end:
            dts = [dt]
            if dt.weekday() >= 5:
                dts.append(dt-onze)
            for d in dts:
                moment = Moment.objects.get_or_create(moment=d)
                if moment[1]:
                    self.stdout.write(u'Création du moment %s' % moment[0])
                for groupe in Groupe.objects.all():
                    for user in groupe.membres.all():
                        dtp = DispoToPlay.objects.get_or_create(moment=moment[0], user=user)
                        if dtp[1]:
                            self.stdout.write(u'Création de la dispo %s' % dtp[0])
                    if (groupe.id == 1 and d.hour == 11) or (groupe.id == 2 and d.hour == 20):
                        groupe.moments.add(moment[0])
                        groupe.save()
                        self.stdout.write(u'Ajout du moment %s au groupe %s' % (moment[0], groupe))
            dt += jour
