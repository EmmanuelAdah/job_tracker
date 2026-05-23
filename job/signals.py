from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Job


@receiver(pre_save, sender=Job)
def format_job_data(sender, instance, **kwargs):
    # Format the job title to title case before saving
    if instance.title:
        instance.title = instance.title.title()
    if instance.role:
        instance.role = instance.role.title()