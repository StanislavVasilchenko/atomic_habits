from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Владелец привычки"""
    message = 'You not have permission to perform this action'

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
