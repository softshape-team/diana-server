from django.utils import timezone
from rest_framework import serializers

from . import models
from .functions import add_tags_and_subtask_to_task


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


class TaskSerializer(serializers.ModelSerializer):
    done = serializers.BooleanField(default=False, write_only=True)

    tags = TagSerializer(many=True, read_only=True)
    with_tag = serializers.ListField(
        child=serializers.CharField(max_length=16),
        write_only=True,
        required=False,
    )

    checklist = SubtaskSerializer(many=True, read_only=True)
    with_subtask = serializers.ListField(
        child=serializers.CharField(max_length=64),
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
        user = self.context["request"].user
        tags_names = validated_data.pop("with_tag", None)
        subtasks_titles = validated_data.pop("with_subtask", None)
        task = super().create(validated_data)

        return add_tags_and_subtask_to_task(user, task, tags_names, subtasks_titles)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        tags_names = validated_data.pop("with_tag", None)
        subtasks_titles = validated_data.pop("with_subtask", None)
        task = super().update(instance, validated_data)

        return add_tags_and_subtask_to_task(user, task, tags_names, subtasks_titles)

    class Meta:
        model = models.Task
        fields = (
            "pk",
            "user",
            "title",
            "note",
            "tags",
            "with_tag",
            "checklist",
            "with_subtask",
            "date",
            "reminder",
            "deadline",
            "done_at",
            "priority",
            "done",
        )
        read_only_fields = ("pk", "user", "tags", "done_at")


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


class HabitLogSerializer(serializers.ModelSerializer):
    def validate_habit(self, habit):
        if habit.user != self.context["request"].user:
            raise serializers.ValidationError("Habit does not exists")

        return habit

    class Meta:
        model = models.HabitLog
        fields = "__all__"


class HabitSerializer(serializers.ModelSerializer):
    history = HabitLogSerializer(many=True, read_only=True)

    def validate_days(self, days):
        if len(days) != len(set(days)):
            raise serializers.ValidationError("Days can not be repeated")

        return days

    class Meta:
        model = models.Habit
        fields = "__all__"
        read_only_fields = ("pk", "user")
