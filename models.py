# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models import CharField, CommaSeparatedIntegerField, DateTimeField, ForeignKey, IntegerField, ManyToManyField, Model, NullBooleanField
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Moment(Model):
    moment = DateTimeField(unique=True)

    class Meta:
        ordering = ["moment"]

    def __str__(self):
        return '%s' % self.moment


@python_2_unicode_compatible
class DispoToPlay(Model):
    moment = ForeignKey(Moment)
    user = ForeignKey(User)
    dispo = NullBooleanField(default=True)

    class Meta:
        unique_together = ("moment", "user")
        ordering = ["moment", "user"]

    def __str__(self):
        if self.dispo:
            return '%s est dispo le %s' % (self.user, self.moment)
        if self.dispo is None:  # TODO: NYI
            return '%s peut essayer d’être dispo le %s' % (self.user, self.moment)
        return '%s n’est pas dispo le %s' % (self.user, self.moment)


@python_2_unicode_compatible
class Groupe(Model):
    nom = CharField(max_length=50, unique=True)
    jours = CommaSeparatedIntegerField(max_length=13)
    debut = IntegerField()  # heure de début
    duree = IntegerField()  # durée d’une partie, en heures
    membres = ManyToManyField(User)
    moments = ManyToManyField(Moment)

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return "Groupe «%s» avec %s" % (self.nom, ', '.join([m.username for m in self.membres.all()]))
