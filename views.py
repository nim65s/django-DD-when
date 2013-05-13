#-*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from when.models import *

from datetime import datetime


def moments_ok(groupe):
    moments = []
    for moment in groupe.moments.filter(moment__gte=datetime.now()):
        for user in groupe.membres.all():  # TODO: aggregate ? En tout cas faut démochifier…
            if DispoToPlay.objects.get_or_create(moment=moment, user=user)[0].dispo is False:
                break
        else:
            moments.append(moment)
            if len(moments) > 9:
                break
    return moments


def home(request):
    groupes = []
    for groupe in request.user.groupe_set.order_by('nom'):
        groupes.append((groupe, moments_ok(groupe)))
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
def groupes(request, id=None):
    if id:
        return render(request, 'when/groupes.html', {'groupes': [get_object_or_404(Groupe, id=id)] })
    return render(request, 'when/groupes.html', {'groupes': Groupe.objects.all()})


@login_required
def dispo(request, moment, dispo):
    dtp = DispoToPlay.objects.get_or_create(user=request.user, moment=Moment.objects.get(id=moment))[0]
    if dispo == '1':
        dtp.dispo = True
        messages.success(request, u"Welcome Back \o/")
    else:
        dtp.dispo = False
        messages.info(request, u"Indisponibilité enregistrée")
    dtp.save()
    if 'next' in request.GET and request.GET['next'] == 'dispos':
        return dispos(request)
    return home(request)


def ics(request, groupe):
    groupe = get_object_or_404(Groupe, pk=groupe)
    c = {
            'nom': groupe.nom,
            'ok': moments_ok(groupe),
            }
    return render(request, 'when/groupe.ics', c, content_type="text/calendar; charset=UTF-8")
