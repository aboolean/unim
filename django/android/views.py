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

class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = (IsOwnerOrAdmin,)

    # @action(methods=['POST','GET'])
    # def profile_complete(self, request, pk=None):
    #     student = self.get_object()

    #     if request.method == 'GET':
    #         return Response({"complete": student.isProfileComplete})
    #     elif request.method == 'POST':
    #         if hasattr(request.DATA, 'complete'):
    #             student.isProfileComplete = request.DATA['complete']
    #             student.save()
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

        # serializer = PasswordSerializer(data=request.DATA)
        # if serializer.is_valid():
        #     user.set_password(serializer.data['password'])
        #     user.save()
        #     return Response({'status': 'password set'})
        # else:
        #     return Response(serializer.errors,
        #                     status=status.HTTP_400_BAD_REQUEST)

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

# class UserViewSet2(viewsets.ViewSet):
#     def list(self, request):
#         pass

#     def create(self, request):
#         pass

#     def retrieve(self, request, pk=None):
#         pass

#     def update(self, request, pk=None):
#         pass

#     def partial_update(self, request, pk=None):
#         pass

#     def destroy(self, request, pk=None):
#         pass

# class MeetupViewSet2(viewsets.ViewSet):
#     def list(self, request):
#         pass

#     def create(self, request):
#         pass

#     def retrieve(self, request, pk=None):
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = serializers.MeetupSerializer(user)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         pass

#     def partial_update(self, request, pk=None):
#         pass

#     def destroy(self, request, pk=None):
#         pass