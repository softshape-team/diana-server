from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import Task, Subtask, Tag, Habit, HabitLog


class TaskTagAdmin(admin.TabularInline):
    model = Task.tags.through


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskTagAdmin]


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    pass
