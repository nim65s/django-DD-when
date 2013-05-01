#-*- coding: utf-8 -*-
#from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from when.models import Moment, DispoToPlay, DispoToPlayForm, get_groupes

from datetime import datetime


def home(request):
    groupes = {}
    for groupe in get_groupes():
        if request.user in groupe.user_set.all():
            group_name = groupe.name[5:].capitalize().replace('_', ' ')
            groupes[group_name] = []
            for moment in Moment.objects.filter(moment__gte=datetime.now()).order_by('moment'):
                for user in groupe.user_set.all():  # TODO: aggregate ? En tout cas faut démochifier…
                    if DispoToPlay.objects.get(moment=moment, user=user).dispo is False:
                        break
                else:
                    groupes[group_name].append(moment)
                    if len(groupes[group_name]) > 4:
                        break
    return render(request, 'when/home.html', {'groupes': groupes})


@login_required
def dispos(request):
    return home(request)  # TODO
    #dispos = DispoToPlay.objects.filter(user=request.user, moment__gte=datetime.now()).order_by('moment')
    #if request.method == 'POST':
        #form = DispoToPlayForm(request.POST)
        #if form.is_valid():
            #form.instance.user = request.user
            #form.save()
    #return render(request, 'when/dispos.html', {'dispos': dispos})


@login_required
def groupes(request):
    return home(request)  # TODO
