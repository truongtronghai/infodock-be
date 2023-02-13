from django.db import models

# Create your models here.
from django.db import models


class Image(models.Model):
    file = models.ImageField(upload_to="upload/%Y/%m/%d/")
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
