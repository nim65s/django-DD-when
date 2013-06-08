#-*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe

from when.models import *

from datetime import datetime, date
from calendar import LocaleHTMLCalendar
from pytz import timezone

tzloc = timezone(settings.TIME_ZONE).localize


def moments_ok(groupe):
    """ Liste les 10 prochains moments OK pour un groupe """
    moments = []
    for moment in groupe.moments.filter(moment__gte=tzloc(datetime.now())):
        for user in groupe.membres.all():
            if DispoToPlay.objects.get(moment=moment, user=user).dispo is False:
                break
        else:
            moments.append(moment)
            if len(moments) > 9:
                break
    return moments


def organise_dispos(dispos):
    """ Prend une liste de dispos et les classe dans un dict avec la date à la clef """
    timetable = dict()
    for dispo in dispos:
        dispo_date = dispo.moment.moment.date()
        if dispo_date in timetable:
            timetable[dispo_date].append(dispo)
        else:
            timetable[dispo_date] = [dispo]
    return timetable


class WhenCalendar(LocaleHTMLCalendar):
    """ Génère un calendrier HTML avec les dispos de tout le monde classées par jour """
    def __init__(self, dispos, user, firstweekday=0, locale=None):
        LocaleHTMLCalendar.__init__(self, firstweekday, locale)
        self.dispos = organise_dispos(dispos)
        moments = [dispo.moment.moment for dispo in dispos]
        self.first_moment = min(moments)
        self.last_moment = max(moments)
        self.user = user

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        retour = '<td class="%s"><p style="text-align: center">%s</p><br>' % (self.cssclasses[weekday], day)
        hour = None
        if date(self.cur_year, self.cur_month, day) in self.dispos:
            for dtp in self.dispos[date(self.cur_year , self.cur_month, day)]:
                m = tzloc(dtp.moment.moment)
                if m.hour != hour:
                    hour = m.hour
                    retour += '<br>%s: ' % m.strftime('%H:%M')
                if dtp.dispo is True:
                    classe = 'green'
                else:
                    classe = 'red'
                if dtp.user == self.user:
                    retour += u'<a href="%s?next=dispos">' % reverse('when:dispo', kwargs={'moment': dtp.moment.id, 'dispo': dtp.dispo.real})
                retour += u'<span style="color:%s">%s</span> ' % (classe, dtp.user)
                if dtp.user == self.user:
                    retour += '</a>'
        retour += '</td>'
        return retour

    def formatwhen(self, withyear=True):
        first_year = self.first_moment.year
        v = []
        a = v.append
        a('<table border="1" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatweekheader())
        if first_year == self.last_moment.year:
            for month in range(self.first_moment.month, self.last_moment.month + 1):
                a(self.formatmonthname(first_year, month, withyear=withyear))
                for week in self.monthdays2calendar(first_year, month):
                    if date(first_year, month, max(week)[0]) >= self.first_moment.date():
                        self.cur_month = month
                        self.cur_year = first_year
                        a(self.formatweek(week))
                        a('\n')
        else:
            pass  # TODO
        return u''.join(v)


def home(request):
    groupes = [(g, moments_ok(g)) for g in request.user.groupe_set.all()]
    return render(request, 'when/home.html', {'groupes': groupes})


@login_required
def dispos(request):
    dispos = DispoToPlay.objects.filter(moment__moment__gte=tzloc(datetime.now()))
    cal = WhenCalendar(dispos=dispos, user=request.user)
    return render(request, 'when/dispos.html', {'cal': mark_safe(cal.formatwhen())})


@login_required
def groupes(request, id=None):
    if id:
        return render(request, 'when/groupes.html', {'groupes': [get_object_or_404(Groupe, id=id)] })
    return render(request, 'when/groupes.html', {'groupes': Groupe.objects.all()})


@login_required
def dispo(request, moment, dispo):
    dtp = DispoToPlay.objects.get_or_create(user=request.user, moment=Moment.objects.get(id=moment))[0]
    if dispo == '0':  # C’est plus simple dans le template comme ça
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
            'groupe': groupe,
            'ok': moments_ok(groupe),
            }
    return render(request, 'when/groupe.ics', c, content_type="text/calendar; charset=UTF-8")
