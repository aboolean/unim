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
from datetime import datetime, timedelta
from django.utils import timezone
import math

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
            # check if complete
            student.isProfileComplete = True
            for e in serializer.data.values():
                if e == None or e == "":
                    student.isProfileComplete = False
            student.save()
            return Response({},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def state(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    content = dict()
    content['isProfileComplete'] = student.isProfileComplete
    now = timezone.now()
    if student.isLooking == True:
        if student.activeUntil == None or now > student.activeUntil:
            student.activeUntil = None
            student.isLooking = False
            student.save()
            content['isLooking'] = False
        else:
            content['isLooking'] = True
            delta = student.activeUntil - now
            content['activeFor'] = delta.total_seconds() / 3600 # hours
    else:
        student.activeUntil = None
        student.save()
    # pending rating
    content['pendingRating'] = student.pendingRating != None # other member
    if content['pendingRating']:
        other = student.pendingRating.owner
        content['ratingName'] = other.first_name + " " + other.last_name
        content['ratingName'] = content['ratingName'][:30]

    # pending match
    content['pendingMatch'] = student.currentMembership != None
    if student.currentMembership != None:
        content['haveAccepted'] = student.currentMembership.accepted is not None # None or True
        content['bothAccepted'] = student.currentMembership.accepted is not None and student.currentMembership.partner.accepted is not None
        content['partnerUnlocked'] = True # change with location
    return Response(content)

@api_view(['POST'])
def match(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if student.currentMembership != None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # check to include appropriate fields
    REQUIRED_FIELDS = ['waitHours', 'waitMins', 'distance', 'locLat', 'locLong', 'radius']

    if sum([1 if e in request.DATA else 0 for e in REQUIRED_FIELDS]) != len(REQUIRED_FIELDS):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    content = dict()

    # update location
    locLat = float(request.DATA['locLat'])
    locLong = float(request.DATA['locLong'])
    radius = float(request.DATA['radius'])
    student.locLat = locLat
    student.locLong = locLong
    student.radiusLooking = radius
    student.save()

    # get all students who are looking
    available = models.Student.objects.filter(isLooking=True)

    # remove expired results and find closest
    closest = (None, 0)
    for stu in available:
        if stu.activeUntil == None or stu.activeUntil < timezone.now():
            stu.activeUntil = None
            stu.isLooking = False
            stu.save()
            continue
        
        dist = 69 * math.sqrt((stu.locLong - locLong)**2 + (stu.locLat - locLat) **2)
        if dist <= student.radiusLooking and dist <= radius:
            if closest[0] == None or closest[1] > dist:
                closest = (stu, dist)

    if closest[0] != None:
        pass
    else:
        content['notFound'] = True
        student.isLooking = True
        student.activeUntil = timezone.now() + timedelta(minutes=float(request.DATA['waitMins'], hours=float(request.DATA['waitHours'])))

    return Response(content)

@api_view(['POST'])
def cancel(request):
    pass

@api_view(['POST'])
def location(request):
    pass

@api_view(['POST'])
def respond(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if 'response' in request.DATA:
        if student.currentMembership == None: # partner decline
            return Response({'matchFail':True})
        content = dict()
        response = request.DATA['response']
        partnerResponse = student.currentMembership.partner.accepted
        if response == True: # Accept
            student.currentMembership.accepted = True
            student.currentMembership.save()
            if partnerResponse == None: # waiting on other
                content['matchFail'] = False
                content['bothAccepted'] = False
            elif partnerResponse == True: # both accepted
                content['matchFail'] = False
                content['bothAccepted'] = True
        elif response == False: # Decline
            student.currentMembership.accepted = False
            student.currentMembership.save()
            student.currentMembership = None
            student.save()
            content['matchFail'] = True
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(content)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def rate(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if 'rating' in request.DATA:
        if student.pendingRating != None:
            partner = student.pendingRating.owner.student
            # rating on meeting member
            student.pendingRating.receivedRating = request.DATA['rating']
            student.pendingRating.save()
            # adjust avg on other user
            num = partner.numReviews
            newRating = 1 if request.DATA['rating'] == True else 0
            total = partner.reliableMatch * num + newRating
            partner.reliableMatch = total / (num + 1)
            partner.numReviews += 1
            partner.save()
            student.pendingRating = None
            student.save()
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def partner(request):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if student.currentMembership != None:
        partner = student.currentMembership.partner
        serializer = serializers.ProfileSerializer(partner, many=False)
        content = serializer.data
        if student.currentMembership.accepted and student.currentMembership.partner.accepted:
            content['name'] = partner.owner.first_name + " " + partner.owner.last_name
        return Response(content)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# BROWSEABLE FUNCTIONS
@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'profile': reverse(profile, request=request, format=format),
        'state': reverse(state, request=request, format=format),
        'match': reverse(match, request=request, format=format),
        'cancel': reverse(cancel, request=request, format=format),
        'respond': reverse(respond, request=request, format=format),
        'rate': reverse(rate, request=request, format=format),
        'partner': reverse(partner, request=request, format=format),
        'location': reverse(location, request=request, format=format),
    })
