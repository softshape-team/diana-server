from django.utils import timezone
from rest_framework import serializers

from . import models


class TaskSerializer(serializers.ModelSerializer):
    done = serializers.BooleanField(default=False, write_only=True)
    with_tags = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
    )

    def validate_with_tags(self, with_tags):
        request = self.context["request"]

        for tag_pk in with_tags:
            if not models.Tag.objects.filter(pk=tag_pk, user=request.user).exists():
                raise serializers.ValidationError(
                    "One or more tags ids is not correct."
                )

        return with_tags

    def validate(self, attrs):
        method = self.context["request"].method
        if method in ["PUT", "PATCH"]:
            if attrs.get("done") == True:
                attrs["done_at"] = timezone.now()
            else:
                attrs["done_at"] = None

        elif method == "POST" and attrs.get("done"):
            raise serializers.ValidationError(
                "You can't create an already completed task."
            )

        try:
            del attrs["done"]
        except Exception:
            pass

        return attrs

    def create(self, validated_data):
        tags_pks = validated_data.pop("with_tags", None)

        task = models.Task.objects.create(**validated_data)

        if not tags_pks:
            return task

        for tag_pk in tags_pks:
            tag = models.Tag.objects.get(pk=tag_pk)
            models.TaskTag.objects.create(task=task, tag=tag)

        task = models.Task.objects.get(pk=task.pk)
        return task

    class Meta:
        model = models.Task
        fields = (
            "pk",
            "user",
            "name",
            "note",
            "tags",
            "with_tags",
            "date",
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
