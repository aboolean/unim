#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import android.models


# FIELDS:
# https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types

# ForeignKey goes in *child*/many class (many-to-one relation)
# parent = ForeignKey(Parent, relative_key="children")

@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        android.models.Student.objects.create(owner=instance)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Student(models.Model):

    """
    Represents single student user and assoicated variables.
    """

    # User includes: Name, email, passwd, username, (verification?)
    owner = models.OneToOneField(User) # user.student = self

    # Profile Fields
    isProfileComplete = models.BooleanField(default=False)
    iAm = models.CharField(max_length=400, blank=True)
    iLike = models.CharField(max_length=400, blank=True)
    iWant = models.CharField(max_length=400, blank=True)
    dorm = models.CharField(max_length=30, blank=True)
    major = models.CharField(max_length=30, blank=True)

    photo = models.CharField(max_length=50, blank=True)

    # Rating System
    pendingRating = models.OneToOneField('Member', related_name='awaiting_raing',null=True, blank=True) # most recent encounter
    reliableMatch = models.FloatField(default=0)  # upvotes
    numReviews = models.IntegerField(default=0)  # total reviews (num meetings)

    # Location (current)
    locLat = models.FloatField(default=999)  # range [-180,180]
    locLong = models.FloatField(default=999) # 999 is null flag

    # Matchmaking
    activeUntil = models.DateTimeField(default=None,blank=True,null=True)  # waiting until
    radiusLooking = models.FloatField(default=0)
    isLooking = models.BooleanField(default=False)  # currently searching/waiting
    partnerUnlocked = models.BooleanField(default=False)

    # Meetup instance
    currentMembership = models.OneToOneField('Member', null=True, blank=True)
    # currentMembership.meetup --> returns current Meetup instance
    # currentMembership.meetup.members.exclude(student=self) --> returns other student
    # currentMembership.student --> always equals self (preserved)

    # IMAGE FIELD

    def __unicode__(self):
        return str(self.owner.username)

class Meetup(models.Model):
    """
    Represents a single meeting between two individuals.
    """
    # Student members
    # self.members.all() for both members

    # Timestamps
    matchTime = models.DateTimeField(auto_now_add=True)
    meetTime = models.DateTimeField(blank=True,null=True)

    # Locations
    location = models.ForeignKey('Location', related_name='meetups')

    class Meta:
        pass

    def __unicode__(self):
        return ", ".join([e.owner.username for e in self.members.all()]) + " -- " + str(self.matchTime)

class Member(models.Model):
    """
    Details related to a single member of a meetup.
    """
    # Lookup all meetups for a user:
    # Student.object.filter(user = u).memberships.meetups
    owner = models.ForeignKey(User, related_name='memberships')
    meetup = models.ForeignKey('Meetup', related_name='members')
    partner = models.OneToOneField('Member', null=True, blank=True)

    # self.student --> returns current student (probably unused backward ref.)

    # Meetup Tacking
    accepted = models.NullBooleanField(default=None)
    responseTime = models.DateTimeField(blank=True,null=True)
    receivedRating = models.NullBooleanField(default=None)

    def __unicode__(self):
        return "%s" % self.owner.username + " -- " + str(self.meetup.matchTime)

class Location(models.Model):
    """
    Represents a single valid meeting location.
    """
    # Coordinates
    locLat = models.FloatField()  # range [-180,180]
    locLong = models.FloatField()

    # Details
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=400)

    def __unicode__(self):
        return "%s, %s" % (self.locLat, self.locLong)

