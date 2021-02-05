from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
]

router = DefaultRouter()

router.register(r"task", views.TaskViewSet, basename="task")
router.register(r"subtask", views.SubtaskViewSet, basename="subtask")
router.register(r"tag", views.TagViewSet, basename="tag")
router.register(r"habit", views.HabitViewSet, basename="habit")
router.register(r"habitlog", views.HabitLogViewSet, basename="habitlog")
router.register(r"tasktag", views.TaskTagViewSet, basename="tasktag")

urlpatterns += router.urls
