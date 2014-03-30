#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel, Model

# FIELDS:
# https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types

class Student(TimeStampedModel):

    """
    Represents single student user and assoicated variables.
    """

    # User includes: Name, email, passwd, username, (verification?)
    user = models.OneToOneField(User)

    # Profile Fields
    iAm1 = models.TextField()
    iAm2 = models.TextField()
    iAm3 = models.TextField()
    iLike1 = models.TextField()
    iLike2 = models.TextField()
    iLike3 = models.TextField()
    iWant1 = models.TextField()
    iWant2 = models.TextField()
    iWant3 = models.TextField()

    # Rating System
    hasRatedRecent = models.BooleanField(default=True) # most recent rating
    reliableMatch = models.IntegerField(default=0) # upvotes
    numReviews = models.IntegerField(default=0) # total reviews (num meetings)

    # Location
    locLat = models.FloatField(default=999) # range [-180,180]
    locLong = models.FloatField(default=999)

    # Matchmaking
    activeUntil = models.DateTimeField() # waiting until
    isLooking = models.BooleanField(default=False) # currently searching/waiting
    activeMatch = models.BooleanField(default=False) # pending/completed match

    #IMAGE FIELD

    # def __unicode__(self):
    #     return '%s' % self.# whatever you want this to be, toString

class Meetup(Model):
    users = models.ManyToManyFields('Student', null=True)
    # call meetups=Meetup.users.filter('username') for User
    contactTime = models.DateTimeField(auto_now_add=True)

    # def __unicode__(self):
    #     return '%s' % 'Meeting at ' + str(self.contactTime)
