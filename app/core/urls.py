from django.urls import path

from . import views


urlpatterns = [
    path("task/", views.TaskList.as_view(), name="task-list"),
    path("task/<str:pk>/", views.TaskDetail.as_view(), name="task-detail"),
    path("subtask/", views.SubtaskList.as_view(), name="subtask-list"),
    path("subtask/<str:pk>/", views.SubtaskDetail.as_view(), name="subtask-detail"),
]