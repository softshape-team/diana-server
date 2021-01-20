from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import Task, Tag, Habit, HabitLog


class TaskTagAdmin(admin.TabularInline):
    model = Task.tags.through


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ["done_at"]
    inlines = [TaskTagAdmin]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    pass
