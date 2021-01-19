from rest_framework import permissions

from .models import Task


class OwnSubtask(permissions.BasePermission):
    """
    Return True if the requested subtask owned by the authed user, False otherwise.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user == obj.task.user:
            return False

        return True
