#-*- coding: utf-8 -*-
from django.db.models import Model, ForeignKey, ManyToManyField
from django.db.models import NullBooleanField, DateTimeField, CharField
from django.forms import ModelForm
from django.contrib.auth.models import User, Group


class Moment(Model):
    moment = DateTimeField(unique=True)

    class Meta:
        ordering = ["moment"]

    def __unicode__(self):
        return u'%s' % self.moment


class DispoToPlay(Model):
    moment = ForeignKey(Moment)
    user = ForeignKey(User)
    dispo = NullBooleanField(default=True)

    class Meta:
        unique_together = ("moment", "user")
        ordering = ["moment"]

    def __unicode__(self):
        if self.dispo:
            return u'%s est dispo le %s' % (self.user, self.moment)
        if self.dispo is None:  # TODO: NYI
            return u'%s peut essayer d’être dispo le %s' % (self.user, self.moment)
        return u'%s n’est pas dispo le %s' % (self.user, self.moment)


class DispoToPlayForm(ModelForm):
    class Meta:
        model = DispoToPlay
        exclude = ('user')


class Groupe(Model):
    nom = CharField(max_length=50, unique=True)
    membres = ManyToManyField(User)

    class Meta:
        ordering = ["nom"]

    def __unicode__(self):
        return u"Groupe «%s» avec %s" % (self.nom, ', '.join([m.username for m in self.membres.all()]))

