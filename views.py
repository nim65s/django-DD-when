#-*- coding: utf-8 -*-
#from django.contrib import messages
#from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from when.models import Moment, DispoToPlay, DispoToPlayForm

from datetime import datetime


def home(request):
    moments = Moment.objects.filter(moment__gte=datetime.now()).order_by('moment')
    return render(request, 'when/home.html', {'moments': moments})


@login_required
def dispos(request):
    if request.method == 'POST':
        form = DispoToPlayForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
    dispos = DispoToPlay.objects.filter(user=request.user, moment__gte=datetime.now()).order_by('moment')
    return render(request, 'when/dispos.html', {'dispos': dispos})

@login_required
def groupes(request):
    return home(request)  # TODO

@login_required
def faq(request):
    return home(request)  # TODO
