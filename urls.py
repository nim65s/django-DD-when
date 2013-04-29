from django.conf.urls.defaults import patterns, url
from when.views import *

urlpatterns = patterns('',
        url(r'^$', home, name='home'),
        url(r'^dispos$', dispos, name='dispos'),
        url(r'^groupes$', groupes, name='groupes'),
        url(r'^faq$', faq, name='faq'),
        )

