from django.db import models
import uuid

# Create your models here.

class Job(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False
        )
    
    title = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    description = models.TextField(blank=False)
    contact_email = models.CharField(max_length=100, null=True)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
