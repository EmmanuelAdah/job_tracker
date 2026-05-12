from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Subscription(models.Model):
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
        )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class PackageChoices(models.TextChoices):
        FREE = 'FREE', 'Free'
        BASIC = 'BASIC', 'Basic'
        PREMIUM = 'PREMIUM', 'Premium'

    package = models.CharField(
        max_length=20,
        choices=PackageChoices.choices,
        default=PackageChoices.FREE
    )