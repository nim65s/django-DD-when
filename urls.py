from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from when.views import *

urlpatterns = patterns('',
        url(r'^$', home, name='home'),
        url(r'^dispos$', dispos, name='dispos'),
        url(r'^groupes$', groupes, name='groupes'),
        url(r'^faq$', TemplateView.as_view(template_name='when/faq.html'), name="faq"),
        )
