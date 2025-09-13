from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AbstractBaseModel(models.Model):
    STATUS_CHOISE = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOISE, default="active")
    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Project(AbstractBaseModel):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("archived", "Archived"),
       ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")

    def __str__(self):
        return self.title

class Task(AbstractBaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("overdue", "Overdue"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["due_date"]),
        ]
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.title} ({self.project.title})"
    
class DevelopmentTask(Task):
    programming_language = models.CharField(max_length=50, blank=True)
    repository_url = models.URLField(blank=True)


class DesignTask(Task):
    design_tool = models.CharField(max_length=50, blank=True)
    asset_link = models.URLField(blank=True)




    