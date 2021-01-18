from django.urls import path

from . import views


urlpatterns = [
    path("task/", views.TaskList.as_view(), name="task-list"),
    path("task/<str:pk>/", views.TaskDetail.as_view(), name="task-detail"),
]
