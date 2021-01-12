from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=32,
        validators=[validate_password],
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, value: str):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return email

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "birthdate",
            "daily_progress",
            "password",
        )
        read_only_fields = (
            "pk",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
            "daily_progress",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
