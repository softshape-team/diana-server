from django.urls import path, include

from . import views


urlpatterns = [
    path("registration/", views.Registration.as_view(), name="registration"),
    path("", include("dj_rest_auth.urls")),
]
