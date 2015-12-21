from django.conf.urls import url
from django.views.generic import TemplateView
from when.views import dispo, dispos, groupes, home, ics

app_name = 'when'
urlpatterns = [
        url(r'^$', home, name='home'),
        url(r'^dispos$', dispos, name='dispos'),
        url(r'^dispo/(?P<moment>\d+)/(?P<dispo>\d)/$', dispo, name='dispo'),
        url(r'^groupes$', groupes, name='groupes'),
        url(r'^groupe/(?P<id>\d)/$', groupes, name='groupe'),
        url(r'^(?P<groupe>\d+).ics$', ics, name='ics'),
        url(r'^faq$', TemplateView.as_view(template_name='when/faq.html'), name="faq"),
        ]
