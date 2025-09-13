from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from django.core import mail
from .models import Project, DevelopmentTask, DesignTask
from .tasks import mark_overdue_tasks
from django.conf import settings
settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


class ProjectTaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        from django.conf import settings
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    def test_project_creation(self):
        project = Project.objects.create(
            user=self.user,
            title="Test Project",
            description="Sample project",
            start_date="2025-09-13",
            end_date="2025-09-20",
        )
        self.assertEqual(str(project), "Test Project")

    def test_dev_task_signal_email(self):
        project = Project.objects.create(
            user=self.user,
            title="Signal Project",
            start_date="2025-09-13",
            end_date="2025-09-20",
        )
        task = DevelopmentTask.objects.create(
            project=project,
            title="Dev Task",
            due_date=timezone.now().date(),
            programming_language="Python"
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("New Development Task", mail.outbox[0].subject)

    def test_design_task_signal_email(self):
        project = Project.objects.create(
            user=self.user,
            title="Design Signal Project",
            start_date="2025-09-13",
            end_date="2025-09-20",
        )
        task = DesignTask.objects.create(
            project=project,
            title="Design Task",
            due_date=timezone.now().date(),
            design_tool="Figma"
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("New Design Task", mail.outbox[0].subject)

    def test_project_deletion_signal_email(self):
        project = Project.objects.create(
            user=self.user,
            title="Project To Delete",
            start_date="2025-09-13",
            end_date="2025-09-20",
        )
        DevelopmentTask.objects.create(
            project=project,
            title="Dev Task",
            due_date=timezone.now().date(),
            programming_language="Python"
        )
        DesignTask.objects.create(
            project=project,
            title="Design Task",
            due_date=timezone.now().date(),
            design_tool="Figma"
        )
        mail.outbox = []
        project.delete()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Project Deleted", mail.outbox[0].subject)

class ProjectAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="apiuser", password="password")
        self.project = Project.objects.create(
            user=self.user,
            title="API Project",
            start_date="2025-09-13",
            end_date="2025-09-20",
        )
        # Authenticated client
        self.client.force_authenticate(user=self.user)

    def test_list_projects(self):
        response = self.client.get("/core/api/projects/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], "API Project")

    def test_create_project_authenticated(self):
        data = {
            "user": self.user.id,
            "title": "New Project",
            "description": "Test",
            "start_date": "2025-09-13",
            "end_date": "2025-09-20",
            "status": "planned"
        }
        response = self.client.post("/core/api/projects/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 2)


class CeleryOverdueTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="celeryuser", password="password")
        self.project = Project.objects.create(
            user=self.user,
            title="Celery Project",
            start_date="2025-09-01",
            end_date="2025-09-30",
        )
        

    def test_mark_overdue_tasks(self):
        dev_task = DevelopmentTask.objects.create(
            project=self.project,
            title="Old Dev Task",
            due_date="2025-09-01",
            programming_language="Python"
        )
        design_task = DesignTask.objects.create(
            project=self.project,
            title="Old Design Task",
            due_date="2025-09-01",
            design_tool="Figma"
        )
        mail.outbox = []  
        mark_overdue_tasks()
        dev_task.refresh_from_db()
        design_task.refresh_from_db()
        self.assertEqual(dev_task.status, "overdue")
        self.assertEqual(design_task.status, "overdue")
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn("Task Overdue", mail.outbox[0].subject)
