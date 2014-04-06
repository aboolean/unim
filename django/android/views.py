#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, link
from android import serializers, models
from android.permissions import IsOwnerOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = (permissions.AllowAny,)

    @action(methods=['POST','GET'])
    def profile_complete(self, request, pk=None):
        student = self.get_object()

        if request.method == 'GET':
            return Response({"complete": student.isProfileComplete})
        elif request.method == 'POST':
            if 'complete' in request.DATA:
                student.isProfileComplete = request.DATA['complete']
                student.save()
                return Response({"complete": student.isProfileComplete})
        return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    @link()
    def get_status(self, request, pk=None):
        pass



class MeetupViewSet(viewsets.ModelViewSet):
    queryset = models.Meetup.objects.all()
    serializer_class = serializers.MeetupSerializer
    permission_classes = (IsOwnerOrAdmin,)

class MemberViewSet(viewsets.ModelViewSet):
    queryset = models.Member.objects.all()
    serializer_class = serializers.MemberSerializer
    permission_classes = (IsOwnerOrAdmin,)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)
