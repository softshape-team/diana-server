from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient

from .models import Task, Subtask, Tag
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


class TasksTest(APITestCase):
    def setUp(self) -> None:
        self.users, self.clients = users_clients()

        self.tasks = {
            "sami": [
                Task.objects.create(user=self.users["sami"], name="Foo"),
            ],
            "rami": [
                Task.objects.create(user=self.users["rami"], name="Bar"),
            ],
        }

        self.subtasks = {
            "sami": [
                Subtask.objects.create(task=self.tasks["sami"][0], name="Foo"),
            ],
            "rami": [
                Subtask.objects.create(task=self.tasks["rami"][0], name="Foo"),
            ],
        }

        self.tags = {
            "sami": [
                Tag.objects.create(user=self.users["sami"], name="Home"),
            ],
            "rami": [
                Tag.objects.create(user=self.users["rami"], name="Important"),
            ],
        }

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
        self.assertEqual(len(res.data["results"]), 1)

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
        self.assertEqual(len(res.data["results"]), 2)

    def test_task_detail(self):
        """
        User can only (access, update, delete) his/her task.
        authed user required.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        st0 = self.tasks["sami"][0]

        ########## GET a task ####################
        res = client.get(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 200)

        res = rclient.get(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## PUT a task ####################
        res = client.put(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.put(rvs("task-detail", args=[st0.pk]), {"name": "New name"})
        self.assertEqual(res.status_code, 200)

        res = rclient.put(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## DELETE a task ####################
        res = client.delete(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.delete(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 204)

        res = rclient.delete(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

    def test_subtask_list(self):
        """
        Get task's checklists.
        Add a new subtask.
        Authed user required.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        st0 = self.tasks["sami"][0]

        ########## GET a checklist ####################
        res = client.get(rvs("subtask-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("subtask-list", params={"task": st0.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

        res = rclient.get(rvs("subtask-list", params={"task": st0.pk}))
        self.assertEqual(res.status_code, 404)

        ########## POST a subtask ####################
        res = client.post(rvs("subtask-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.post(rvs("subtask-list"), {"task": st0.pk, "name": "Foo"})
        self.assertEqual(res.status_code, 201)

        res = rclient.post(rvs("subtask-list"), {"task": st0.pk, "name": "Bar"})
        self.assertEqual(res.status_code, 400)

        ########## GET all again ####################
        res = sclient.get(rvs("subtask-list", params={"task": st0.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 2)

    def test_subtask_detail(self):
        """
        Get, Update, Delete a task's subtasks.
        Authed user required.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        sst0 = self.subtasks["sami"][0]

        ########## GET a subtask ####################
        res = client.get(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 200)

        res = rclient.get(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## PUT a subtask ####################
        res = client.put(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.put(
            rvs("subtask-detail", args=[sst0.pk]),
            {
                "task": sst0.task.pk,
                "name": "something",
                "done": False,
            },
        )
        self.assertEqual(res.status_code, 200)

        res = rclient.put(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## GET a subtask again ####################
        res = sclient.get(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], "something")

        ########## DELETE a subtask again ####################
        res = client.delete(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 401)

        res = rclient.delete(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 404)

        res = sclient.delete(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 204)

    def test_tag_list(self):
        """
        User can get his/her tags.
        User can add a new tag.
        Authed user required.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()

        ########## GET all tags ####################
        res = client.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

        res = rclient.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

        ########## POST a new tag ####################
        res = client.post(rvs("tag-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.post(rvs("tag-list"), {"name": "foo"})
        self.assertEqual(res.status_code, 201)

        ########## Get all tags again ####################
        res = sclient.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 2)

        res = rclient.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

    def test_tag_detail(self):
        """
        User can retrieve, update and delete his/her tags only.
        Authed user is required.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        st0 = self.tags["sami"][0]

        ########## GET a tag ####################
        res = client.get(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 200)

        res = rclient.get(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## PUT a tag ####################
        res = client.put(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.put(rvs("tag-detail", args=[st0.pk]), {"name": "foo"})
        self.assertEqual(res.status_code, 200)

        res = rclient.put(rvs("tag-detail", args=[st0.pk]), {"name": "foo"})
        self.assertEqual(res.status_code, 404)

        ########## DELETE a tag ####################
        res = client.delete(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = rclient.delete(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

        res = sclient.delete(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 204)
