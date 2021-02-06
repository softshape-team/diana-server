import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from core.validators import BothIncludedRangeValidator


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    email = models.EmailField(unique=True, max_length=32, null=False, blank=False)
    username = models.CharField(
        unique=True,
        max_length=16,
        validators=[
            RegexValidator(r"^[a-zA-Z0-9_]*$"),
        ],
    )

    password = models.CharField(max_length=128)

    birthdate = models.DateField(null=True, blank=True)
    daily_progress = models.FloatField(
        default=0, validators=[BothIncludedRangeValidator(0, 100)]
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    timezone = models.CharField(max_length=32, null=True, blank=True)

    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def clean(self, *args, **kwargs):
        self.email = self.email.lower()
        super().clean(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        ordering = ("username",)

        indexes = (
            models.Index(fields=("username",)),
            models.Index(fields=("email",)),
        )

        constraints = (
            models.CheckConstraint(
                name="valid_daily_progress",
                check=models.Q(daily_progress__gte=0)
                & models.Q(daily_progress__lte=100),
            ),
        )
