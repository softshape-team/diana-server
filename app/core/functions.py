from django.utils import timezone
from django.urls import reverse
from .models import Task


def rvs(name, *, args=None, kwargs=None, params: dict = None):
    first = reverse(name, args=args, kwargs=kwargs)

    if params is None:
        return first

    second = "?"
    for param in params.items():
        second += f"{param[0]}={param[1]}&"

    second = second[:-1]
    return first + second


def task_pk_validator(request, task_pk):
    if not task_pk:
        return False

    task = Task.objects.filter(pk=task_pk).first()
    if not task:
        return False

    if task.user != request.user:
        return False

    return True


def update_daily_progress(user):
    """
    Update user's daily progress
    """

    today_tasks = Task.objects.filter(user=user, date=timezone.now().date())
    if not today_tasks.count():
        return

    todo = today_tasks.filter(done_at__isnull=True).count()
    done = today_tasks.filter(done_at__isnull=False).count()

    user.daily_progress = (done / (todo + done)) * 100
    user.save()

    return user.daily_progress
