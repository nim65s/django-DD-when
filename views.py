#-*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe

from when.models import *

from datetime import datetime, date, timedelta
from calendar import LocaleHTMLCalendar
from pytz import timezone

tz = timezone(settings.TIME_ZONE)
tzloc = tz.localize


try:
    WHEN_ADD_MONTH_DAYS = settings.WHEN_ADD_MONTH_DAYS
except:
    WHEN_ADD_MONTH_DAYS = 30


def moments_ok(groupe, n_max=None):
    """ Liste les 10 prochains moments OK pour un groupe """
    moments = []
    seen = {}
    n_membres = len(groupe.membres.all())
    for m in groupe.moments.filter(dispotoplay__dispo=True, moment__gte=tzloc(datetime.now())):
        if m not in seen:
            seen[m] = 1
        else:
            seen[m] += 1
            if seen[m] == n_membres:
                moments.append(m)
                if n_max and len(moments) >= n_max:
                    break
    else:
        if n_max:
            add_month()

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
                m = dtp.moment.moment.astimezone(tz)
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


@login_required
def home(request):
    groupes = [(g, moments_ok(g, n_max=10)) for g in request.user.groupe_set.all()]
    return render(request, 'when/home.html', {'groupes': groupes})


@login_required
def dispos(request):
    dispos = DispoToPlay.objects.filter(moment__moment__gte=tzloc(datetime.now()),
            moment__dispotoplay__user=request.user)
    cal = WhenCalendar(dispos=dispos, user=request.user)
    return render(request, 'when/dispos.html', {'cal': mark_safe(cal.formatwhen())})


@login_required
def groupes(request, id=None):
    if id:
        groupes = [get_object_or_404(Groupe, id=id)]
    else:
        groupes = request.user.groupe_set.all()
    return render(request, 'when/groupes.html', {'groupes': groupes})


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
    g = get_object_or_404(Groupe, pk=groupe)
    return render(request, 'when/groupe.ics', {'groupe': g, 'ok': moments_ok(g)}, content_type="text/calendar; charset=UTF-8")


def add_month():
    now = datetime.now()
    then = now + timedelta(days=WHEN_ADD_MONTH_DAYS)
    end = tzloc(datetime(then.year, then.month, 1))

    for groupe in Groupe.objects.all():
        dt = tzloc(datetime(now.year, now.month, 1))
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
            dt += timedelta(1)
