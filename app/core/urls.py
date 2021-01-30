from django.urls import path

from . import views


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("task/", views.TaskList.as_view(), name="task-list"),
    path("task/<str:pk>/", views.TaskDetail.as_view(), name="task-detail"),
    path("subtask/", views.SubtaskList.as_view(), name="subtask-list"),
    path("subtask/<str:pk>/", views.SubtaskDetail.as_view(), name="subtask-detail"),
    path("tag/", views.TagList.as_view(), name="tag-list"),
    path("tag/<str:pk>/", views.TagDetail.as_view(), name="tag-detail"),
    path("tasktag/", views.TaskTagList.as_view(), name="tasktag-list"),
    path("tasktag/<str:pk>/", views.TaskTagDetail.as_view(), name="tasktag-detail"),
    path("habit/", views.HabitList.as_view(), name="habit-list"),
    path("habit/<str:pk>/", views.HabitDetail.as_view(), name="habit-detail"),
    path("habitlog/", views.HabitLogList.as_view(), name="habitlog-list"),
]
