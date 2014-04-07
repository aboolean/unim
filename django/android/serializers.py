#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from android import models
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):

#     memberships = serializers.PrimaryKeyRelatedField(many=True)

#     class Meta:

#         model = User
#         fields = (
#             'url',
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'student',
#             )

# class StudentSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:

#         model = models.Student
#         fields = (
#             'url',
#             'owner',
#             'isProfileComplete',
#             'iAm',
#             'iLike',
#             'iWant',
#             'locLat',
#             'locLong',
#             'activeUntil',
#             'isLooking',
#             'pendingMatch',
#             'currentMembership',
#             )

# class MeetupSerializer(serializers.HyperlinkedModelSerializer):

#     members = serializers.PrimaryKeyRelatedField(many=True)

#     class Meta:

#         model = models.Meetup
#         fields = ('url', 'members', 'matchTime', 'meetTime', 'location')

# class MemberSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:

#         model = models.Member
#         fields = (
#             'url',
#             'owner',
#             'meetup',
#             'accepted',
#             'responseTime',
#             'receivedRating',
#             )

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
