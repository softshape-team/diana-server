from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from . import models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"
        read_only_fields = ("pk", "user", "tags", "done_at")


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subtask
        fields = "__all__"
        read_only_fields = ("pk",)

    def validate_task(self, task):
        if self.context["request"].user != task.user:
            raise serializers.ValidationError("Task does not exists")

        return task


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"
        read_only_fields = ("user",)


class TaskTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskTag
        fields = "__all__"
        read_only_fields = ["pk"]

    def validate(self, attrs):
        user = self.context["request"].user

        if attrs["task"].user != user or attrs["tag"].user != user:
            raise serializers.ValidationError(
                "User should be the owner of the task and the tag."
            )

        return attrs
