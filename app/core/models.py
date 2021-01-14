import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .validators import BothIncludedRangeValidator


User = get_user_model()


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Priority(models.IntegerChoices):
    P0 = 0
    P1 = 1
    P2 = 2
    P3 = 3


class Color(models.IntegerChoices):
    GREY = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    PINK = 5
    ORANGE = 6


class Tag(Base):
    user = models.ForeignKey(User, related_name="tags", on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    color = models.IntegerField(choices=Color.choices, default=0)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["user", "name"]

        indexes = [
            models.Index(fields=["user"]),
        ]


class Task(Base):
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    note = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="tasks", through="TasksTags")
    deadline = models.DateTimeField(null=True, blank=True)
    done_at = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(
        choices=Priority.choices,
        default=0,
        validators=[BothIncludedRangeValidator(0, 3)],
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["user"]

        indexes = [
            models.Index(fields=["user"]),
        ]

        constraints = [
            models.CheckConstraint(
                name="valid_priority",
                check=models.Q(priority__gte=0) & models.Q(priority__lte=3),
            ),
        ]


class Checklist(Base):
    task = models.ForeignKey(Task, related_name="checklist", on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class TasksTags(Base):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.SET_DEFAULT, default=0)

    def __str__(self):
        return f"{self.task} - {self.tag}"

    def clean(self):
        if self.task.user != self.tag.user:
            raise ValidationError(
                "Tasks can only be linked to tags from the same user."
            )

    class Meta:
        ordering = ["tag"]

        indexes = [
            models.Index(fields=["task"]),
            models.Index(fields=["tag"]),
        ]
