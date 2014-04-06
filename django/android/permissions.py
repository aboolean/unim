#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins and owners to edit.
    """

    def has_object_permission(self, request, view, obj):
        if permissions.IsAdminUser in request.user.user_permissions.all():
            return True

        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'members'):
            for member in obj.members.all():
                if member.owner == request.user:
                    return True

        return False