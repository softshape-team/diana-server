from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import Task, Tag, Habit


class TasksTagsAdmin(admin.TabularInline):
    model = Task.tags.through


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TasksTagsAdmin]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass
