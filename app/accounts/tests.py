from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import Task


User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.users = {
            "sami": User.objects.create_user(
                username="sami",
                email="sami@example.com",
                password="goodpass",
            ),
            "rami": User.objects.create_user(
                username="rami",
                email="rami@example.com",
                password="goodpass",
            ),
        }

    def test_daily_progress(self):
        self.assertEqual(self.users["sami"].daily_progress, 100)
        self.assertEqual(self.users["rami"].daily_progress, 100)

        sami0 = Task.objects.create(
            user=self.users["sami"], name="Hello", date=timezone.now().date()
        )
        self.assertEqual(User.objects.get(username="sami").daily_progress, 0)

        sami1 = Task.objects.create(
            user=self.users["sami"], name="Hello", date=timezone.now().date()
        )
        self.assertEqual(User.objects.get(username="sami").daily_progress, 0)

        sami2 = Task.objects.create(
            user=self.users["sami"], name="Hello", date=timezone.now().date()
        )
        self.assertEqual(User.objects.get(username="sami").daily_progress, 0)

        sami3 = Task.objects.create(
            user=self.users["sami"], name="Hello", date=timezone.now().date()
        )
        self.assertEqual(User.objects.get(username="sami").daily_progress, 0)

        sami4 = Task.objects.create(user=self.users["sami"], name="Hello")
        self.assertEqual(User.objects.get(username="sami").daily_progress, 0)

        sami0.done_at = timezone.now()
        sami0.save()
        self.assertEqual(User.objects.get(username="sami").daily_progress, 25)

        sami1.done_at = timezone.now()
        sami1.save()
        self.assertEqual(User.objects.get(username="sami").daily_progress, 50)

        sami1.delete()
        sami2.delete()
        self.assertEqual(User.objects.get(username="sami").daily_progress, 50)

        sami3.done_at = timezone.now()
        sami3.save()
        self.assertEqual(User.objects.get(username="sami").daily_progress, 100)

        self.assertEqual(User.objects.get(username="rami").daily_progress, 100)

        sami0.delete()
        self.assertEqual(User.objects.get(username="sami").daily_progress, 100)

        rami0 = Task.objects.create(
            user=self.users["rami"], name="Hello", date=timezone.now().date()
        )
        self.assertEqual(User.objects.get(username="rami").daily_progress, 0)
        rami0.done_at = timezone.now()
        rami0.save()
        self.assertEqual(User.objects.get(username="rami").daily_progress, 100)

        self.assertEqual(User.objects.get(username="sami").daily_progress, 100)
