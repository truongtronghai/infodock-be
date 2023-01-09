from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class FcmRegistrationId(models.Model):
    DEVICE_TYPES = [
        ("ios", "iOs"),
        ("android", "Android"),
        ("web", "Web"),
    ]
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)

    registrationId = models.CharField(max_length=200, default="", unique=True)
    deviceType = models.CharField(
        max_length=10, choices=DEVICE_TYPES, default="android"
    )
