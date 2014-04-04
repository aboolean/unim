#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# FIELDS:
# https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types

# ForeignKey goes in *child*/many class (many-to-one relation)
# parent = ForeignKey(Parent, relative_key="children")

class Student(models.Model):

    """
    Represents single student user and assoicated variables.
    """

    # User includes: Name, email, passwd, username, (verification?)

    user = models.OneToOneField(User)

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

    activeUntil = models.DateTimeField(default=datetime.now(),blank=True)  # waiting until
    isLooking = models.BooleanField(default=False)  # currently searching/waiting
    pendingMatch = models.BooleanField(default=False)  # pending/completed match

    # Meetup instance
    currentMembership = models.OneToOneField('MeetupMember', null=True)
    # currentMembership.meetup --> returns current Meetup instance
    # currentMembership.meetup.members.exclude(student=self) --> returns other student
    # currentMembership.student --> always equals self (preserved)

    # IMAGE FIELD

    # def __unicode__(self):
    #     return '%s' % self.# whatever you want this to be, toString

class Meetup(models.Model):
    """
    Represents a single meeting between two individuals.
    """
    # Student members
    # meetup.members.all() for both members

    # Timestamps
    matchTime = models.DateTimeField(auto_now_add=True)
    meetTime = models.DateTimeField(blank=True,null=True)

    # Locations
    location = models.ForeignKey('MeetingLocation', related_name='meetups')

    # def __unicode__(self):
    #     return '%s' % self.# whatever you want this to be, toString

class MeetupMember(models.Model):
    """
    Details related to a single member of a meetup.
    """
    # Lookup all meetups for a user:
    # Student.object.filter(user = u).memberships.meetups
    studentMember = models.ForeignKey('Student', related_name='memberships')
    meetup = models.ForeignKey('Meetup', related_name='members')

    # self.student --> returns current student (probably unused backward ref.)

    # Meetup Tacking
    accepted = models.NullBooleanField(default=None)
    responseTime = models.DateTimeField(blank=True,null=True)
    receivedRating = models.NullBooleanField(default=None)

    # def __unicode__(self):
    #     return '%s' % self.# whatever you want this to be, toString

class MeetingLocation(models.Model):
    """
    Represents a single valid meeting location.
    """
    # Coordinates
    locLat = models.FloatField()  # range [-180,180]
    locLong = models.FloatField()

class TestIt(models.Model):
    date = models.DateTimeField(blank=True,null=True)
    boolean = models.NullBooleanField(default=None)
    floatNum = models.FloatField(default=0)
    intNum = models.IntegerField(default=0)
    strField = models.CharField(max_length=160, blank=True)
