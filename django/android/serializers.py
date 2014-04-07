#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from android import models
from rest_framework import serializers

class LocationSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Location
        fields = ('locLat', 'locLong')

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Student
        fields = ('iAm', 'iLike', 'iWant', 'dorm', 'major')


class StateSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Student
        fields = ('isProfileComplete', 'activeUntil', 'isLooking')
