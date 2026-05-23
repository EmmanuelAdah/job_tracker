from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be occupied')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True,
        editable=False
        )
    

    validate_name = RegexValidator(r'^[a-zA-Z]+$', 'Only letters are allowed in names.')
    
    first_name = models.CharField(max_length=50, blank=False, validators=[validate_name])
    last_name = models.CharField(max_length=50, blank=False, validators=[validate_name])
    email = models.EmailField(unique=True, max_length=100, blank=False)
    bio = models.TextField(max_length=1000, blank=True)

    applied_jobs = models.ManyToManyField('job.Job', blank=True, related_name='applicants')
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

