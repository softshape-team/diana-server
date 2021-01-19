from rest_framework import serializers

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
