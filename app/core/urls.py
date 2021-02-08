from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r"", views.Index, basename="index")
router.register(r"task", views.TaskViewSet, basename="task")
router.register(r"subtask", views.SubtaskViewSet, basename="subtask")
router.register(r"tag", views.TagViewSet, basename="tag")
router.register(r"habit", views.HabitViewSet, basename="habit")
router.register(r"habitlog", views.HabitLogViewSet, basename="habitlog")
router.register(r"tasktag", views.TaskTagViewSet, basename="tasktag")

urlpatterns = router.urls
