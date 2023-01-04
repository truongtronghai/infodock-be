import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="userprofile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    id = models.UUIDField(
        primary_key=True, unique=True, null=False, blank=False, default=uuid.uuid4
    )
    avatar = models.ImageField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
