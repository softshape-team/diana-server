from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # TODO: PUT request does not work -- split the serializer into 2 ?
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=32,
        validators=[validate_password],
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, value: str):
        return value.lower()

    def validate(self, data):
        if self.context["request"].method in ("PUT", "PATCH") and "password" in data:
            raise serializers.ValidationError("You can not set a new password.")

        return data

    class Meta:
        model = User
        fields = (
            "pk",
            "first_name",
            "last_name",
            "username",
            "email",
            "birthdate",
            "timezone",
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
