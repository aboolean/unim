#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from android.models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = User
        fields = ('url', 'username', 'email', 'groups')


class TestItSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestIt
        fields = ('date','boolean','floatNum','intNum','strField')
