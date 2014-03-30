#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# FIELDS:
# https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types

class Student(models.Model):

    """
    Represents single student user and assoicated variables.
    """

    # User includes: Name, email, passwd, username, (verification?)

    user = models.OneToOneField(User)

    # Profile Fields

    iAm1 = models.CharField(max_length=160)
    iAm2 = models.CharField(max_length=160, blank=True)
    iAm3 = models.CharField(max_length=160, blank=True)
    iLike1 = models.CharField(max_length=160)
    iLike2 = models.CharField(max_length=160, blank=True)
    iLike3 = models.CharField(max_length=160, blank=True)
    iWant1 = models.CharField(max_length=160)
    iWant2 = models.CharField(max_length=160, blank=True)
    iWant3 = models.CharField(max_length=160, blank=True)

    # Rating System

    hasRatedRecent = models.BooleanField(default=True)  # most recent rating
    reliableMatch = models.IntegerField(default=0)  # upvotes
    numReviews = models.IntegerField(default=0)  # total reviews (num meetings)

    # Location

    locLat = models.FloatField(default=999)  # range [-180,180]
    locLong = models.FloatField(default=999)

    # Matchmaking

    activeUntil = models.DateTimeField(default=datetime.now(),blank=True)  # waiting until
    isLooking = models.BooleanField(default=False)  # currently searching/waiting
    activeMatch = models.BooleanField(default=False)  # pending/completed match


    # IMAGE FIELD

    # def __unicode__(self):
    #     return '%s' % self.# whatever you want this to be, toString

class Meetup(models.Model):

    users = models.ManyToManyField('Student', null=True)

    # call meetups=Meetup.users.filter('username') for User

    contactTime = models.DateTimeField(auto_now_add=True)


    # def __unicode__(self):
    #     return '%s' % 'Meeting at ' + str(self.contactTime)
