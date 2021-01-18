from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from . import serializers, models


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
