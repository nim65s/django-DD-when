from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from when.views import *

urlpatterns = patterns('',
        url(r'^$', home, name='home'),
        url(r'^dispos$', dispos, name='dispos'),
        url(r'^dispo/(?P<moment>\d+)/(?P<dispo>\d)/$', dispo, name='dispo'),
        url(r'^groupes$', groupes, name='groupes'),
        url(r'^groupe/(?P<id>\d)/$', groupes, name='groupe'),
        #url(r'^cal_(?P<groupe>\d+).ics$', ics, name='ics'),
        url(r'^faq$', TemplateView.as_view(template_name='when/faq.html'), name="faq"),
        )
