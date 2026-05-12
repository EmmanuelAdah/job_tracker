from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CustomUser


@receiver(pre_save, sender=CustomUser)
def format_user_data(sender, instance, **kwargs):
    if instance.first_name:
        instance.first_name = instance.first_name.upper()
    if instance.last_name:
        instance.last_name = instance.last_name.upper()
    if instance.email:
        instance.email = instance.email.lower()