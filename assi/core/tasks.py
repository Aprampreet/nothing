# core/tasks.py
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import DevelopmentTask, DesignTask

@shared_task
def mark_overdue_tasks():
    today = timezone.now().date()
    dev_tasks = DevelopmentTask.objects.filter(status__in=['pending','in_progress'], due_date__lt=today)
    for task in dev_tasks:
        task.status = 'overdue'
        task.save()
        send_mail(
            subject=f"Task Overdue: {task.title}",
            message=f"Your development task '{task.title}' in project '{task.project.title}' is now overdue.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[task.project.user.email],
        )
    design_tasks = DesignTask.objects.filter(status__in=['pending','in_progress'], due_date__lt=today)
    for task in design_tasks:
        task.status = 'overdue'
        task.save()
        send_mail(
            subject=f"Task Overdue: {task.title}",
            message=f"Your design task '{task.title}' in project '{task.project.title}' is now overdue.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[task.project.user.email],
        )

    print(f"Marked {dev_tasks.count()} development and {design_tasks.count()} design tasks as overdue.")
