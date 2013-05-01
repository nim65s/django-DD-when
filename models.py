#-*- coding: utf-8 -*-
from django.db.models import Model, ForeignKey, NullBooleanField, DateTimeField
from django.forms import ModelForm
from django.contrib.auth.models import User, Group


def get_groupes():
    return Group.objects.filter(name__startswith='when')


class Moment(Model):
    moment = DateTimeField(unique=True)

    def __unicode__(self):
        return u'%s' % self.moment


class DispoToPlay(Model):
    moment = ForeignKey(Moment)
    user = ForeignKey(User)
    dispo = NullBooleanField(default=True)

    class Meta:
        unique_together = ("moment", "user")

    def __unicode__(self):
        if self.dispo:
            return u'%s est dispo le %s' % (self.user, self.moment)
        if self.dispo is None:
            return u'%s peut essayer d’être dispo le %s' % (self.user, self.moment)
        return u'%s n’est pas dispo le %s' % (self.user, self.moment)


class DispoToPlayForm(ModelForm):
    class Meta:
        model = DispoToPlay
        exclude = ('user')
