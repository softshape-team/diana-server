from django.contrib import admin

from .models import Task, Tag


class TasksTagsAdmin(admin.TabularInline):
    model = Task.tags.through


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TasksTagsAdmin]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
