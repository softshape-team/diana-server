from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from . import models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"
        read_only_fields = ("user", "done_at")
