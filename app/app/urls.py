from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    # Admin App
    path("admin/", admin.site.urls),
    # Core app
    # Accounts app
    path("accounts/", include("accounts.urls")),
    # API Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "dev/api/ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "dev/api/docs/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
