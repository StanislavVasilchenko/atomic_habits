from rest_framework import permissions


class IsHabitOwner(permissions.BasePermission):
    message = 'You do not have permission to view this resource'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
