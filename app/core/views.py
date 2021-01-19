from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers, models
from .permissions import OwnSubtask
from .functions import task_pk_validator


class TaskList(generics.ListCreateAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SubtaskList(generics.ListCreateAPIView):
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
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
