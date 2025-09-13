from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Project, DevelopmentTask, DesignTask
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=DevelopmentTask)
def dev_task_created(sender, instance, created, **kwargs):
    if created:
        print(f"New Development Task: {instance.title}")
        send_mail(
            subject=f"New Development Task: {instance.title}",
            message=f"A new development task '{instance.title}' was created for your project '{instance.project.title}'.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.project.user.email],
        )

@receiver(post_save, sender=DesignTask)
def design_task_created(sender, instance, created, **kwargs):
    if created:
        print(f"New Design Task: {instance.title}")
        send_mail(
            subject=f"New Design Task: {instance.title}",
            message=f"A new design task '{instance.title}' was created for your project '{instance.project.title}'.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.project.user.email],
        )

@receiver(pre_delete, sender=Project)
def project_deleted(sender, instance, **kwargs):
    dev_count = instance.developmenttask_set.count()
    design_count = instance.designtask_set.count()
    total = dev_count + design_count

    send_mail(
        subject="Project Deleted",
        message=f"Your project '{instance.title}' has been deleted along with {total} tasks.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.user.email],
    )

    print(f"Project '{instance.title}' is being deleted along with {total} tasks")

