from rest_framework import serializers

from . import models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"
        read_only_fields = ("pk", "user", "tags", "done_at")
