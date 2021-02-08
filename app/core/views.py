from django.db.models import query
from django.views import View
from django.shortcuts import render


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers, models


class Index(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Welcome to diana api.",
            },
            status=200,
        )


class TaskViewSet(viewsets.ModelViewSet):
    """
    LC: authed user can do LC to his account only.
    RUD: authed user can do RUD for his/her tasks only.
    """

    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubtaskViewSet(viewsets.ModelViewSet):
    """
    LC: authed user can do LC to his account only.
    RUD: authed user can do RUD to his/her subtasks only.
    """

    serializer_class = serializers.SubtaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Subtask.objects.all()

    def get_queryset(self):
        return self.queryset.filter(task__user=self.request.user)

    def perform_create(self, serializer):
        if self.request.method in ("PUT", "PATCH"):
            task = self.request.query_params.get("task")
            serializer.save(task=task)
            return

        return super().perform_create(serializer)


class TagViewSet(viewsets.ModelViewSet):
    """
    LC: authed user can do LC to his account only.
    RUD: authed user can do RUD to his account only.
    """

    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitViewSet(viewsets.ModelViewSet):
    """
    LC: authed user can do LC to his account only.
    RUD: authed user can do RUD to his account only.
    """

    serializer_class = serializers.HabitSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Habit.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitLogViewSet(viewsets.ModelViewSet):
    """
    LC: authed user can LC to his account only.
    filtering supported: specify habit=pk to filter habitlog by the habit.
    """

    serializer_class = serializers.HabitLogSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.HabitLog.objects.all()

    def get_queryset(self):
        res = self.queryset.filter(habit__user=self.request.user)
        params = self.request.query_params
        if "habit" in params:
            res = res.filter(habit=params["habit"])

        return res

    def retrieve(self, request, *args, **kwargs):
        return Response(status=405)

    def update(self, request, *args, **kwargs):
        return Response(status=405)

    def destroy(self, request, *args, **kwargs):
        return Response(status=405)


class TaskTagViewSet(viewsets.ModelViewSet):
    """
    L: not allowed.
    C: authed user can create a new tasktag linked with (task, tag) belong to him/her.
    D: Customize deletion allowed where authed user can delete a task
    by providing the task id and the tag id as URLs params.
    """

    serializer_class = serializers.TaskTagSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.TaskTag.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(task__user=user, tag__user=user)

    def delete(self, request):
        query_params = request.query_params

        try:
            task = models.Task.objects.get(pk=query_params.get("task"))
            tag = models.Tag.objects.get(pk=query_params.get("tag"))
            tasktag = models.TaskTag.objects.get(
                task=task,
                tag=tag,
                task__user=request.user,
                tag__user=request.user,
            )

            tasktag.delete()
            return Response(status=204)

        except (
            models.Task.DoesNotExist,
            models.Tag.DoesNotExist,
            models.TaskTag.DoesNotExist,
        ):
            return Response(status=404)

    def list(self, request, *args, **kwargs):
        return Response(status=405)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=405)

    def update(self, request, *args, **kwargs):
        return Response(status=405)

    def destroy(self, request, *args, **kwargs):
        return Response(status=405)
