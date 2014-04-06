#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from android import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    memberships = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:

        model = User
        fields = (
            'url',
            'username',
            'email',
            'first_name',
            'last_name',
            'student',
            )


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = models.Student
        fields = (
            'url',
            'owner',
            'currentMembership',
            'locLat',
            'locLong',
            'activeUntil',
            'isLooking',
            'pendingMatch',
            )


class MeetupSerializer(serializers.HyperlinkedModelSerializer):

    members = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:

        model = models.Meetup
        fields = ('url', 'members', 'matchTime', 'meetTime', 'location')


class MemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = models.Member
        fields = (
            'url',
            'owner',
            'meetup',
            'accepted',
            'responseTime',
            'receivedRating',
            )


class LocationSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Location
        fields = ('locLat', 'locLong')
