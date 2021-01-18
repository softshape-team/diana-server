from re import L
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import serializers, models
from .permissions import OwnChecklist, OwnSubtask


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
    permission_classes = (IsAuthenticated, OwnChecklist)
    queryset = models.Subtask.objects.all()

    def get_queryset(self):
        task = self.request.query_params.get("task")
        return self.queryset.filter(task__user=self.request.user).filter(task=task)

    def perform_create(self, serializer):
        task = self.request.query_params.get("task")
        serializer.save(task=task)


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
