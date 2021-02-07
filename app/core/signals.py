from django.utils.timezone import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Task
from .functions import update_daily_progress


@receiver(post_save, sender=Task)
def update_daily_progress_after_saving_task(sender, instance, created, **kwargs):
    update_daily_progress(instance.user)


@receiver(post_delete, sender=Task)
def update_daily_progress_after_deleting_task(sender, instance, **kwargs):
    update_daily_progress(instance.user)
