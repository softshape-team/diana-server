from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=32,
        validators=[validate_password],
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "birthdate",
            "password",
        )
        read_only_fields = (
            "pk",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

        def validate_email(self, value: str):
            email = value.lower()
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    "A user with this email already exists."
                )

            return email


class UserSerializer(RegistrationSerializer):
    class Meta:
        exclude = ("password",)

    def create(self, validated_data):
        return

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)

        instance.save()
        return instance
