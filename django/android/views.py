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


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class StudentViewSet(viewsets.ModelViewSet):
#     queryset = models.Student.objects.all()
#     serializer_class = serializers.StudentSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     @action(methods=['POST','GET'])
#     def profile_complete(self, request, pk=None):
#         student = self.get_object()

#         if request.method == 'GET':
#             return Response({"complete": student.isProfileComplete})
#         elif request.method == 'POST':
#             if 'complete' in request.DATA:
#                 student.isProfileComplete = request.DATA['complete']
#                 student.save()
#                 return Response({"complete": student.isProfileComplete})
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#         serializer = PasswordSerializer(data=request.DATA)
#         if serializer.is_valid():
#             user.set_password(serializer.data['password'])
#             user.save()
#             return Response({'status': 'password set'})
#         else:
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)
#     @link()
#     def get_status(self, request, pk=None):
#         pass

#     @link()
#     def get_me(self,request,pk=None):
#         pass



# class MeetupViewSet(viewsets.ModelViewSet):
#     queryset = models.Meetup.objects.all()
#     serializer_class = serializers.MeetupSerializer
#     permission_classes = (IsOwnerOrAdmin,)

# class MemberViewSet(viewsets.ModelViewSet):
#     queryset = models.Member.objects.all()
#     serializer_class = serializers.MemberSerializer
#     permission_classes = (IsOwnerOrAdmin,)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)

###############

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly,])
def profile(request):
    if not request.user.is_authenticated():
        Response(status=status.HTTP_403_FORBIDDEN)

    try:
        student = models.Student.objects.get(owner=request.user)
    except models.Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ProfileSerializer(student, many=False)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.ProfileSerializer(student, data=request.DATA, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly,])
def get_state(request):
    pass


# BROWSEABLE FUNCTIONS
@api_view(('GET',))
@permission_classes([permissions.IsAuthenticated,])
def api_root(request, format=None):
    return Response({
        'profile': reverse(profile, request=request, format=format),
    })

# class StudentMe(generics.ListAPIView):
#     serializer_class = serializers.StudentSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def get_queryset(self):
#         user = self.request.user
#         return models.Student.objects.filter(owner=user)
