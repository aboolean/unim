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
    # TODO: permissions

    # Profile Fields

    isProfileComplete = models.BooleanField(default=False)
    iAm1 = models.CharField(max_length=160, blank=True)
    iAm2 = models.CharField(max_length=160, blank=True)
    iAm3 = models.CharField(max_length=160, blank=True)
    iLike1 = models.CharField(max_length=160, blank=True)
    iLike2 = models.CharField(max_length=160, blank=True)
    iLike3 = models.CharField(max_length=160, blank=True)
    iWant1 = models.CharField(max_length=160, blank=True)
    iWant2 = models.CharField(max_length=160, blank=True)
    iWant3 = models.CharField(max_length=160, blank=True)

    # Rating System

    hasRatedRecent = models.BooleanField(default=True)  # most recent rating
    reliableMatch = models.FloatField(default=0)  # upvotes
    numReviews = models.IntegerField(default=0)  # total reviews (num meetings)

    # Location

    locLat = models.FloatField(default=999)  # range [-180,180]
    locLong = models.FloatField(default=999)

    # Matchmaking

    activeUntil = models.DateTimeField(default=datetime.now(),blank=True,required=False)  # waiting until
    isLooking = models.BooleanField(default=False)  # currently searching/waiting
    pendingMatch = models.BooleanField(default=False)  # pending/completed match

    # Meetup instance
    currentMeetup = models.ForeignKey('Meetup', null=True)
    currentMemberSelf = models.ForeignKey('MeetupMember', null=True)
    currentMemberOther = models.ForeignKey('MeetupMember', null=True)

    # IMAGE FIELD

    # def __unicode__(self):
    #     return '%s' % self.# whatever you want this to be, toString

class Meetup(models.Model):

    # Student members
    userA = models.ForeignKey('MeetupMember')
    userB = models.ForeignKey('MeetupMember')

    # Timestamps
    matchTime = models.DateTimeField(auto_now_add=True)
    meetTime = models.DateTimeField(blank=True,null=True,required=False)

    # def __unicode__(self):
    #     return '%s' % 'Meeting at ' + str(self.contactTime)

class MeetupMember(models.Model):
    student = models.ForeignKey('Student')
    accepted = models.NullBooleanField(default=None)
    responseTime = meetTime = models.DateTimeField(blank=True,null=True,required=False)
