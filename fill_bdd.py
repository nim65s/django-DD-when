#-*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group

from when.models import Moment, DispoToPlay, get_groupes

from datetime import datetime, timedelta
from pytz import timezone

tz = timezone('Europe/Paris')

dt = tz.localize(datetime(2013,5,1,20))
end = tz.localize(datetime(2013,7,1,20))

jour = timedelta(1)

while dt < end:
    moment = Moment.objects.get_or_create(moment=dt)
    if moment[1]:
        print u'Création du moment %s' % moment[0]
    for groupe, group_name in get_groupes():
        for user in groupe.user_set.all():
            dtp = DispoToPlay.objects.get_or_create(moment=moment[0], user=user)
            if dtp[1]:
                print u'Création de la dispo %s' % dtp[0]
    dt += jour
