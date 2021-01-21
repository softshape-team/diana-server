from django.db.models import query
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers, models
from .permissions import OwnSubtask
from .functions import task_pk_validator


class TaskList(generics.ListCreateAPIView):
    """
    Authed user can get its own tasks only.
    Authed user can add new task to his account only.
    """

    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Authed user can only (access, update, delete) his/her task.
    """

    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SubtaskList(generics.ListCreateAPIView):
    """
    Authed user can get his/her task's checklist by specifing the task as URL parameter.
    Authed user can add to its checklist.
    """

    serializer_class = serializers.SubtaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Subtask.objects.all()

    def get_queryset(self):
        task = self.request.query_params.get("task")
        return self.queryset.filter(task__user=self.request.user).filter(task=task)

    def perform_create(self, serializer):
        if self.request.method in ("PUT", "PATCH"):
            task = self.request.query_params.get("task")
            serializer.save(task=task)
            return

        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        task_pk = self.request.query_params.get("task")
        if not task_pk_validator(request, task_pk):
            return Response(status=404)

        return super().list(request, *args, **kwargs)


class SubtaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Authed user can Get, Update, Delete a only his/her task's subtasks.
    """

    serializer_class = serializers.SubtaskSerializer
    permission_classes = (IsAuthenticated, OwnSubtask)
    queryset = models.Subtask.objects.all()

    def get_queryset(self):
        res = self.queryset.filter(task__user=self.request.user)
        task = self.request.query_params.get("task")
        if task:
            res = res.filter(task=task)

        return res


class TagList(generics.ListCreateAPIView):
    """
    Authed user can get his/her tags only.
    Authed user can add a new tag to his account only.
    """

    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Authed user can retrieve, update and delete his/her tags only.
    """

    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TaskTagList(generics.CreateAPIView):
    """
    Get tasktags is not allowed.
    Authed user can create a new tasktag linked with (task, tag) belong to him/her.
    """

    serializer_class = serializers.TaskTagSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.TaskTag.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(task__user=user, tag__user=user)


class TaskTagDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Authed user can get, update and delete a task-tag, allowed only for the owner of the of task-tag.
    """

    serializer_class = serializers.TaskTagSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.TaskTag.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(task__user=user, tag__user=user)


class HabitList(generics.ListCreateAPIView):
    serializer_class = serializers.HabitSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Habit.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.HabitSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Habit.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class HabitLogList(generics.ListCreateAPIView):
    serializer_class = serializers.HabitLogSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.HabitLog.objects.all()

    def get_queryset(self):
        res = self.queryset.filter(habit__user=self.request.user)
        params = self.request.query_params
        if "habit" in params:
            res = res.filter(habit=params["habit"])

        return res
