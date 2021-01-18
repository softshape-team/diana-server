from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APIClient

from .models import Task
from .functions import rvs

User = get_user_model()


def users_clients() -> tuple:
    users = {
        "sami": User.objects.create_user(
            username="sami", email="sami@tempmail.softshape.dev", password="goodpass"
        ),
        "rami": User.objects.create_user(
            username="rami", email="rami@tempmail.softshape.dev", password="goodpass"
        ),
    }

    def clients():
        client = APIClient()
        sclient = APIClient()
        rclient = APIClient()
        sclient.force_authenticate(users["sami"])
        rclient.force_authenticate(users["rami"])

        return client, sclient, rclient

    return users, clients


class TasksTest(TestCase):
    def setUp(self) -> None:
        self.users, self.clients = users_clients()

    def test_task_list(self):
        """
        A user can get its own tasks only.
        A user can add new task to his account only.
        authed user required
        """

        # Getting ready
        client, sclient, _ = self.clients()

        ########## GET all ####################
        res = client.get(rvs("task-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("task-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 0)

        ########## POST new ####################
        res = client.post(rvs("task-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.post(
            rvs("task-list"),
            {
                "name": "Foo",
                "reminders": [timezone.now(), timezone.now()],
            },
        )
        self.assertEqual(res.status_code, 201)

        ########## GET all again ####################
        res = sclient.get(rvs("task-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

    def test_task_detail(self):
        """
        User can only (access, update, delete) his/her task.
        authed user required.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        s0 = Task.objects.create(user=self.users["sami"], name="Foo")
        r0 = Task.objects.create(user=self.users["rami"], name="Bar")

        ########## GET a task ####################
        res = client.get(rvs("task-detail", args=[s0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("task-detail", args=[s0.pk]))
        self.assertEqual(res.status_code, 200)

        res = rclient.get(rvs("task-detail", args=[s0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## PUT a task ####################
        res = client.put(rvs("task-detail", args=[s0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.put(rvs("task-detail", args=[s0.pk]), {"name": "New name"})
        self.assertEqual(res.status_code, 200)

        res = rclient.put(rvs("task-detail", args=[s0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## DELETE a task ####################
        res = client.delete(rvs("task-detail", args=[s0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.delete(rvs("task-detail", args=[s0.pk]))
        self.assertEqual(res.status_code, 204)

        res = rclient.delete(rvs("task-detail", args=[s0.pk]))
        self.assertEqual(res.status_code, 404)
