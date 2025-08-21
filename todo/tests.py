from django.test import TestCase
from django.utils import timezone
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APITestCase

from todo.models import Task
from todo.services import apply_status_effects



class ServicesTests(TestCase):
    def test_apply_status_sets_completed_at_when_done(self):
        task = Task.objects.create(title="A", status="todo")
        apply_status_effects(task, "done")
        # služba sama neukládá – jen upraví instanci
        self.assertEqual(task.status, "done")
        self.assertIsNotNone(task.completed_at)

    def test_apply_status_clears_completed_at_when_not_done(self):
        task = Task.objects.create(title="B", status="done", completed_at=timezone.now())
        apply_status_effects(task, "in_progress")
        self.assertEqual(task.status, "in_progress")
        self.assertIsNone(task.completed_at)





class TaskApiTests(APITestCase):
    def test_create_todo_has_no_completed_at(self):
        url = reverse("task-list")
        resp = self.client.post(url, {"title": "Buy milk", "status": "todo"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["status"], "todo")
        self.assertIsNone(resp.data["completed_at"])

    def test_create_done_sets_completed_at(self):
        url = reverse("task-list")
        resp = self.client.post(url, {"title": "Ship", "status": "done"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["status"], "done")
        self.assertIsNotNone(resp.data["completed_at"])

    def test_patch_status_toggles_completed_at(self):
        # vytvoření todo
        create = self.client.post(reverse("task-list"), {"title": "X", "status": "todo"}, format="json")
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        task_id = create.data["id"]

        # status -> done (doplní se completed_at)
        detail = reverse("task-detail", args=[task_id])
        to_done = self.client.patch(detail, {"status": "done"}, format="json")
        self.assertEqual(to_done.status_code, status.HTTP_200_OK)
        self.assertEqual(to_done.data["status"], "done")
        self.assertIsNotNone(to_done.data["completed_at"])

        # status -> in_progress (vynuluje se completed_at)
        to_ip = self.client.patch(detail, {"status": "in_progress"}, format="json")
        self.assertEqual(to_ip.status_code, status.HTTP_200_OK)
        self.assertEqual(to_ip.data["status"], "in_progress")
        self.assertIsNone(to_ip.data["completed_at"])

    def test_filter_status_done(self):
        Task.objects.create(title="A", status="todo")
        Task.objects.create(title="B", status="done")
        Task.objects.create(title="C", status="in_progress")

        url = reverse("task-list") + "?status=done"
        resp = self.client.get(url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.data.get("results", resp.data)  # s/bez pagination
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["status"], "done")
