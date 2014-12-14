# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count


class Command(BaseCommand):
    args = ''
    help = 'Donne le champ TO si on veut envoyer un mail à tout le monde'

    def handle(self, *args, **options):
        liste = ['%s %s <%s>' % (u.first_name, u.last_name, u.email) for u in User.objects.annotate(num_groups=Count('groupe')).filter(num_groups__gt=0)]
        self.stdout.write(', '.join(liste))
