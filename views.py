#-*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404

from when.models import *

from datetime import datetime


def moments_ok(groupe):
    moments = []
    for moment in Moment.objects.filter(moment__gte=datetime.now()).order_by('moment'):
        for user in groupe.user_set.all():  # TODO: aggregate ? En tout cas faut démochifier…
            if DispoToPlay.objects.get_or_create(moment=moment, user=user)[0].dispo is False:
                break
        else:
            moments.append(moment)
            if len(moments) > 9:
                break
    return moments


def home(request):
    groupes = {}
    for groupe, group_name in get_groupes():
        if request.user in groupe.user_set.all():
            groupes[(group_name, groupe.id)] = moments_ok(groupe)
    return render(request, 'when/home.html', {'groupes': groupes})


@login_required
def dispos(request):
    dispos = DispoToPlay.objects.filter(moment__moment__gte=datetime.now()).order_by('moment')
    #if request.method == 'POST':
        #form = DispoToPlayForm(request.POST)
        #if form.is_valid():
            #form.instance.user = request.user
            #form.save()
    return render(request, 'when/dispos.html', {'dispos': dispos})


@login_required
def groupes(request):
    return render(request, 'when/groupes.html', {'groupes': get_groupes()})


@login_required
def pasdispo(request, moment):
    dtp = DispoToPlay.objects.get_or_create(user=request.user, moment=Moment.objects.get(id=moment))[0]
    dtp.dispo = False
    dtp.save()
    messages.info(request, u"Indisponibilité enregistrée")
    if 'next' in request.GET and request.GET['next'] == 'dispos':
        return dispos(request)
    return home(request)


@login_required
def dispo(request, moment):
    dtp = DispoToPlay.objects.get_or_create(user=request.user, moment=Moment.objects.get(id=moment))[0]
    dtp.dispo = True
    dtp.save()
    messages.success(request, u"Welcome Back \o/")
    if 'next' in request.GET and request.GET['next'] == 'dispos':
        return dispos(request)
    return home(request)


def ics(request, groupe):
    groupe = get_object_or_404(Group, pk=groupe)
    c = {
            'groupe': groupe,
            'group_name': group_name(groupe),
            'ok': moments_ok(groupe),
            }
    return render(request, 'when/groupe.ics', c, content_type="text/calendar")  # TODO charset
