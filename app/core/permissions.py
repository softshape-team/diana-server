from rest_framework import permissions

from .models import Task


class OwnChecklist(permissions.BasePermission):
    """
    Return True if the task specified as GET parameter is owned by the user, False otherwise.
    """

    status_code = 404  # TODO: Does not work

    def has_permission(self, request, view):
        task_pk = request.query_params.get("task")
        if not task_pk:
            return False

        task = Task.objects.filter(pk=task_pk).first()
        if not task:
            return False

        if request.user != task.user:
            return False

        return True


class OwnSubtask(permissions.BasePermission):
    """
    Return True if the requested subtask owned by the authed user, False otherwise.
    """

    status_code = 404  # TODO: does not work

    def has_object_permission(self, request, view, obj):
        if not request.user == obj.task.user:
            return False

        return True
