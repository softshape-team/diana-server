import uuid

from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient

from .models import Task, Subtask, Tag, TaskTag, Habit, HabitLog
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
    def setUp(self):
        self.users, self.clients = users_clients()

        self.tasks = {
            "sami": [
                Task.objects.create(user=self.users["sami"], title="Foo"),
            ],
            "rami": [
                Task.objects.create(user=self.users["rami"], title="Bar"),
            ],
        }

        self.subtasks = {
            "sami": [
                Subtask.objects.create(task=self.tasks["sami"][0], title="Foo"),
            ],
            "rami": [
                Subtask.objects.create(task=self.tasks["rami"][0], title="Foo"),
            ],
        }

        self.tags = {
            "sami": [
                Tag.objects.create(user=self.users["sami"], name="Home"),
                Tag.objects.create(user=self.users["sami"], name="Important"),
            ],
            "rami": [
                Tag.objects.create(user=self.users["rami"], name="Important"),
            ],
        }

        self.tasktags = {
            "sami": [
                TaskTag.objects.create(
                    task=self.tasks["sami"][0],
                    tag=self.tags["sami"][0],
                )
            ]
        }

    def test_task_list(self):
        """
        Authed user can get its own tasks only.
        Authed user can add new task to his account only.
        """

        # Getting ready
        client, sclient, _ = self.clients()

        ########## List ####################
        res = client.get(rvs("task-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("task-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

        ########## Create ####################
        res = client.post(rvs("task-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.post(
            rvs("task-list"),
            {
                "title": "Foo",
                "reminder": timezone.now() + timedelta(days=1),
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(res.data["tags"]), 0)

        res = sclient.post(
            rvs("task-list"),
            {
                "title": "Foo",
                "reminder": timezone.now() + timedelta(days=1),
                "with_tag": ["First"],
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(res.data["tags"]), 1)

        res = sclient.post(
            rvs("task-list"),
            {
                "title": "Foo",
                "reminder": timezone.now() + timedelta(days=1),
                "with_tag": ["First", "Second"],
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(res.data["tags"]), 2)

        res = sclient.post(
            rvs("task-list"),
            {
                "title": "Bar",
                "reminder": timezone.now() - timedelta(days=1),
            },
        )
        self.assertEqual(res.status_code, 400)

        res = sclient.post(
            rvs("task-list"),
            {
                "title": "Other",
                "deadline": timezone.now() - timedelta(days=1),
            },
        )
        self.assertEqual(res.status_code, 400)

        res = sclient.post(
            rvs("task-list"),
            {
                "title": "Other task to be created",
                "done": True,
            },
        )
        self.assertEqual(res.status_code, 400)

    def test_task_detail(self):
        """
        Authed user can only (access, update, delete) his/her task.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        st0 = self.tasks["sami"][0]

        ########## Retrieve ####################
        res = client.get(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 200)

        res = rclient.get(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## Update ####################
        res = client.put(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.put(rvs("task-detail", args=[st0.pk]), {"title": "New name"})
        self.assertEqual(res.status_code, 200)

        res = sclient.put(
            rvs("task-detail", args=[st0.pk]), {"title": "New name", "done": True}
        )
        self.assertEqual(res.status_code, 200)

        res = rclient.put(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## Destroy ####################
        res = sclient.get(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["done_at"])

        ########## Destroy ####################
        res = client.delete(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.delete(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 204)

        res = rclient.delete(rvs("task-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

    def test_subtask_list(self):
        """
        Authed user can get his/her subtask only.
        Authed user can add to its checklist.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        st0 = self.tasks["sami"][0]

        ########## List ####################
        res = client.get(rvs("subtask-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("subtask-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

        ########## Create ####################
        res = client.post(rvs("subtask-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.post(rvs("subtask-list"), {"task": st0.pk, "title": "Foo"})
        self.assertEqual(res.status_code, 201)

        res = sclient.post(
            rvs("subtask-list"),
            {"task": st0.pk, "title": "Something new", "done": True},
        )
        self.assertEqual(res.status_code, 400)

        res = rclient.post(rvs("subtask-list"), {"task": st0.pk, "title": "Bar"})
        self.assertEqual(res.status_code, 400)

        ########## List ####################
        res = sclient.get(rvs("subtask-list", params={"task": st0.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 2)

    def test_subtask_detail(self):
        """
        Authed user can Get, Update, Delete a only his/her task's subtasks.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        sst0 = self.subtasks["sami"][0]

        ########## Retrieve ####################
        res = client.get(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 200)

        res = rclient.get(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## Update ####################
        res = client.put(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.put(
            rvs("subtask-detail", args=[sst0.pk]),
            {
                "task": sst0.task.pk,
                "title": "something",
                "done": False,
            },
        )
        self.assertEqual(res.status_code, 200)

        res = rclient.put(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## Retrieve again ####################
        res = sclient.get(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["title"], "something")

        ########## Destroy ####################
        res = client.delete(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 401)

        res = rclient.delete(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 404)

        res = sclient.delete(rvs("subtask-detail", args=[sst0.pk]))
        self.assertEqual(res.status_code, 204)

    def test_tag_list(self):
        """
        Authed user can get his/her tags only.
        Authed user can add a new tag to his account only.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()

        ########## List ####################
        res = client.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 2)

        res = rclient.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

        ########## Create ####################
        res = client.post(rvs("tag-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.post(rvs("tag-list"), {"name": "foo"})
        self.assertEqual(res.status_code, 201)

        res = sclient.post(rvs("tag-list"), {"name": "foo"})
        self.assertEqual(res.status_code, 400)

        ########## List again ####################
        res = sclient.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 3)

        res = rclient.get(rvs("tag-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

    def test_tag_detail(self):
        """
        Authed user can retrieve, update and delete his/her tags only.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        st0 = self.tags["sami"][0]

        ########## Retrieve ####################
        res = client.get(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 200)

        res = rclient.get(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

        ########## Update ####################
        res = client.put(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.put(rvs("tag-detail", args=[st0.pk]), {"name": "foo"})
        self.assertEqual(res.status_code, 200)

        res = rclient.put(rvs("tag-detail", args=[st0.pk]), {"name": "foo"})
        self.assertEqual(res.status_code, 404)

        ########## Destroy ####################
        res = client.delete(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 401)

        res = rclient.delete(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 404)

        res = sclient.delete(rvs("tag-detail", args=[st0.pk]))
        self.assertEqual(res.status_code, 204)

    def test_task_tag_m2m_list(self):
        """
        Get tasktags is not allowed.
        Authed user can create a new tasktag linked with (task, tag) belong to him/her.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()

        sami_tasktag = self.tasktags["sami"][0]
        sami_task = self.tasks["sami"][0]
        sami_tag = self.tags["sami"][0]
        sami_other_tag = self.tags["sami"][1]

        rami_task = self.tasks["rami"][0]
        rami_tag = self.tags["rami"][0]

        ########## List ####################
        # TODO: Review
        res = client.get(rvs("tasktag-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("tasktag-list"))
        self.assertEqual(res.status_code, 405)

        ########## Create ####################
        res = client.post(rvs("tasktag-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.post(
            rvs("tasktag-list"), {"task": sami_task.pk, "tag": sami_tag.pk}
        )
        self.assertEqual(res.status_code, 400)

        res = sclient.post(
            rvs("tasktag-list"), {"task": sami_task.pk, "tag": sami_other_tag.pk}
        )
        self.assertEqual(res.status_code, 201)

        res = rclient.post(
            rvs("tasktag-list"), {"task": rami_task.pk, "tag": sami_tag.pk}
        )
        self.assertEqual(res.status_code, 400)

        res = rclient.post(
            rvs("tasktag-list"), {"task": sami_task.pk, "tag": rami_tag.pk}
        )
        self.assertEqual(res.status_code, 400)

        ########## Delete ####################
        res = client.delete(rvs("tasktag-list"))
        self.assertEqual(res.status_code, 401)

        res = rclient.delete(
            rvs(
                "tasktag-list",
                params={
                    "task": sami_tasktag.task.pk,
                    "tag": sami_tasktag.tag.pk,
                },
            )
        )
        self.assertEqual(res.status_code, 404)

        res = sclient.delete(
            rvs(
                "tasktag-list",
                params={
                    "task": sami_tasktag.task.pk,
                    "tag": sami_tasktag.tag.pk,
                },
            )
        )
        self.assertEqual(res.status_code, 204)


class HabitTest(APITestCase):
    def setUp(self):
        self.users, self.clients = users_clients()

        self.habits = {
            "sami": [
                Habit.objects.create(user=self.users["sami"], title="Foo"),
                Habit.objects.create(user=self.users["sami"], title="Bar"),
            ],
            "rami": [
                Habit.objects.create(user=self.users["rami"], title="Foo"),
            ],
        }

        self.habit_log = {
            "sami": [
                HabitLog.objects.create(
                    habit=self.habits["sami"][0], done_at=timezone.now()
                ),
                HabitLog.objects.create(
                    habit=self.habits["sami"][1], done_at=timezone.now()
                ),
            ]
        }

    def test_habit_list(self):
        """
        Authed user can list his habits only.
        Authed user can create a new habit associate with his account only.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()

        ########## List ####################
        res = client.get(rvs("habit-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("habit-list"))
        self.assertEqual(res.status_code, 200)

        res = rclient.get(rvs("habit-list"))
        self.assertEqual(res.status_code, 200)

        ########## Create ####################
        res = client.post(rvs("habit-list"), {})
        self.assertEqual(res.status_code, 401)

        res = sclient.post(rvs("habit-list"), {"title": "Bar"})
        self.assertEqual(res.status_code, 201)

        res = rclient.post(rvs("habit-list"), {"title": "Bar"})
        self.assertEqual(res.status_code, 201)

        res = sclient.post(rvs("habit-list"), {"title": "Something", "days": [0, 1, 2]})
        self.assertEqual(res.status_code, 201)

        res = sclient.post(rvs("habit-list"), {"title": "Something", "days": [0, 1, 1]})
        self.assertEqual(res.status_code, 400)

        res = sclient.post(rvs("habit-list"), {"title": "Something", "days": [0, 7]})
        self.assertEqual(res.status_code, 400)

        ########## List again ####################
        res = sclient.get(rvs("habit-list"))
        self.assertEqual(len(res.data["results"]), 4)

    def test_habit_detail(self):
        """
        Authed user can (retrieve, update, delete) his habits only.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        sh = self.habits["sami"][0]

        ########## Retrieve ####################
        res = client.get(rvs("habit-detail", args=[sh.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("habit-detail", args=[sh.pk]))
        self.assertEqual(res.status_code, 200)

        res = rclient.get(rvs("habit-detail", args=[sh.pk]))
        self.assertEqual(res.status_code, 404)

        ########## Update ####################
        res = client.put(rvs("habit-detail", args=[sh.pk]))
        self.assertEqual(res.status_code, 401)

        res = sclient.put(rvs("habit-detail", args=[sh.pk]), {"title": "Orange"})
        self.assertEqual(res.status_code, 200)

        res = sclient.put(
            rvs("habit-detail", args=[sh.pk]),
            {
                "title": "Orange",
                "days": [1, 7],
            },
        )
        self.assertEqual(res.status_code, 400)

        res = rclient.put(rvs("habit-detail", args=[sh.pk]))
        self.assertEqual(res.status_code, 404)

        ########## Delete ####################
        res = client.delete(rvs("habit-detail", args=[sh.pk]))
        self.assertEqual(res.status_code, 401)

        res = rclient.delete(rvs("habit-detail", args=[sh.pk]))
        self.assertEqual(res.status_code, 404)

        res = sclient.delete(rvs("habit-detail", args=[sh.pk]))
        self.assertEqual(res.status_code, 204)

        ########## List again ####################
        res = sclient.get(rvs("habit-list"))
        self.assertEqual(len(res.data["results"]), 1)

    def test_habitlog_list(self):
        """
        Authed user can list his habitlog only.
        Authed user can create a new habit log => This is equal to mark a habit as paracticed.
        filtering supported: specify habit=pk to filter habitlog by the habit.
        """

        # Gettings ready
        client, sclient, rclient = self.clients()
        sh0 = self.habits["sami"][0]
        shl0 = self.habit_log["sami"][0]

        ########## List ####################
        res = client.get(rvs("habitlog-list"))
        self.assertEqual(res.status_code, 401)

        res = sclient.get(rvs("habitlog-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 2)

        res = sclient.get(rvs("habitlog-list", params={"habit": sh0.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]["id"], str(shl0.pk))

        res = rclient.get(rvs("habitlog-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 0)

        ########## Create ####################
        res = client.post(rvs("habitlog-list"), {})
        self.assertEqual(res.status_code, 401)

        res = sclient.post(rvs("habitlog-list"), {"habit": sh0.pk})
        self.assertEqual(res.status_code, 201)

        res = rclient.post(rvs("habitlog-list"), {"habit": sh0.pk})
        self.assertEqual(res.status_code, 400)

        res = rclient.post(rvs("habitlog-list"), {"habit": uuid.uuid4()})
        self.assertEqual(res.status_code, 400)

        ########## List again ####################
        res = sclient.get(rvs("habitlog-list"))
        self.assertEqual(len(res.data["results"]), 3)
