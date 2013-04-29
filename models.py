#-*- coding: utf-8 -*-
from django.db.models import Model, ForeignKey, NullBooleanField, DateTimeField
from django.forms import ModelForm
from django.contrib.auth.models import User

class Moment(Model):
    moment = DateTimeField()

    def __unicode__(self):
        return u'%s' % self.moment

class Dispo(Model):
    moment = ForeignKey(Moment)
    user = ForeignKey(User)
    dispo = NullBooleanField()

    def __unicode__(self):
        if dispo:
            return u'%s est dispo le %s' % (self.user, self.moment)
        if dispo is None:
            return u'%s peut essayer d’être dispo le %s' % (self.user, self.moment)
        return u'%s n’est pas dispo le %s' % (self.user, self.moment)

class DispoForm(ModelForm):
    class Meta:
        model = Dispo
        exclude = ('user')
