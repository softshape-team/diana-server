from django.utils import timezone
from rest_framework import serializers

from . import models


class TaskSerializer(serializers.ModelSerializer):
    done = serializers.BooleanField(default=False, write_only=True)

    def validate(self, attrs):
        method = self.context["request"].method
        if method in ["PUT", "PATCH"] and attrs.get("done"):
            attrs["done_at"] = timezone.now()

        elif method == "POST" and attrs.get("done"):
            raise serializers.ValidationError(
                "You can't create an already completed task."
            )

        del attrs["done"]

        return attrs

    class Meta:
        model = models.Task
        fields = (
            "pk",
            "user",
            "name",
            "note",
            "tags",
            "datetime",
            "reminder",
            "deadline",
            "done_at",
            "priority",
            "done",
        )
        read_only_fields = ("pk", "user", "tags", "done_at")


class SubtaskSerializer(serializers.ModelSerializer):
    def validate_task(self, task):
        if self.context["request"].user != task.user:
            raise serializers.ValidationError("Task does not exists")

        return task

    def validate_done(self, done):
        if self.context["request"].method == "POST" and done:
            raise serializers.ValidationError(
                "Done field can not be set on POST request."
            )

        return done

    class Meta:
        model = models.Subtask
        fields = "__all__"
        read_only_fields = ("pk",)


class TagSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        user = self.context["request"].user
        try:
            models.Tag.objects.get(user=user, name=attrs["name"])
            raise serializers.ValidationError("You already have this tag registered.")
        except models.Tag.DoesNotExist:
            return attrs

    class Meta:
        model = models.Tag
        fields = "__all__"
        read_only_fields = ("user",)


class TaskTagSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        request = self.context["request"]

        if attrs["task"].user != request.user or attrs["tag"].user != request.user:
            raise serializers.ValidationError(
                "User should be the owner of the task and the tag."
            )

        return attrs

    class Meta:
        model = models.TaskTag
        fields = "__all__"
        read_only_fields = ["pk"]


class HabitSerializer(serializers.ModelSerializer):
    def validate_days(self, days):
        if len(days) != len(set(days)):
            raise serializers.ValidationError("Days can not be repeated")

        return days

    class Meta:
        model = models.Habit
        fields = "__all__"
        read_only_fields = ("pk", "user")


class HabitLogSerializer(serializers.ModelSerializer):
    def validate_habit(self, habit):
        if habit.user != self.context["request"].user:
            raise serializers.ValidationError("Habit does not exists")

        return habit

    class Meta:
        model = models.HabitLog
        fields = "__all__"
