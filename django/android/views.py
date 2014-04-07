#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions, generics, authentication
from rest_framework.response import Response
# from rest_framework.request import Request
from rest_framework.decorators import action, link, api_view, permission_classes, authentication_classes
from android import serializers, models
from android.permissions import IsOwnerOrAdmin
from rest_framework.reverse import reverse

@api_view(['GET','POST'])
def profile(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ProfileSerializer(student, many=False)
        content = serializer.data
        content['name'] = request.user.first_name + " " + request.user.last_name
        return Response(content)
    elif request.method == 'POST':
        serializer = serializers.ProfileSerializer(student, data=request.DATA, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def state(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.StateSerializer(student, many=False)
    content = serializer.data
    # pending rating
    content['pendingRating'] = student.pendingRating != None # other member
    if content['pendingRating']:
        other = student.pendingRating.owner
        content['ratingName'] = other.first_name + " " + other.last_name
        content['ratingName'] = content['ratingName'][:30]
    # pending match
    content['pendingMatch'] = student.currentMembership != None
    if student.currentMembership != None:
        content['haveAccepted'] = student.currentMembership.accepted # None or True
    return Response(content)

@api_view(['POST'])
def match(request):
    pass

@api_view(['POST'])
def respond(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    pass

@api_view(['POST'])
def rate(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if hasattr(request.DATA):
        pass

# BROWSEABLE FUNCTIONS
@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'profile': reverse(profile, request=request, format=format),
        'state': reverse(state, request=request, format=format),
    })
