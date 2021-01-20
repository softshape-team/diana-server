from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import TokenProxy

from .forms import UserCreationForm, UserChangeForm


User = get_user_model()


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("username", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login")
    fieldsets = (
        (
            "Main Information",
            {
                "fields": ("username", "first_name", "last_name"),
            },
        ),
        (
            "Contact Information",
            {
                "fields": ("email",),
            },
        ),
        (
            "Accounts State",
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        (
            "Dates",
            {
                "fields": ("birthdate", "date_joined", "last_login"),
            },
        ),
        (
            "Other",
            {
                "fields": ("daily_progress", "timezone"),
            },
        ),
    )

    add_fieldsets = (
        (
            "Main Information",
            {
                "fields": ("username", "first_name", "last_name"),
            },
        ),
        (
            "Contact Information",
            {
                "fields": ("email",),
            },
        ),
        (
            "Password",
            {
                "fields": ("password1", "password2"),
            },
        ),
    )
