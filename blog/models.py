from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        # related_name="parent_category", # comment this to use category_set. If related_name existed, category_set is unknown and we have to use related_name to access reverse relation
    )

    name = models.CharField(
        max_length=200, null=False, blank=False, default="New category"
    )
    slug = models.SlugField(max_length=200, null=False, blank=False)

    def delete(self, *args, **kwargs):
        if self.id == 1:  # preventing to delete default category
            return
        else:
            super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        null=False,
        blank=False,
        default=1,
        related_name="posts_in_category",
        on_delete=models.SET_DEFAULT,
    )

    title = models.CharField(
        max_length=200, null=False, blank=False, default="Untitled post"
    )
    slug = models.SlugField(max_length=200, null=False, blank=False)
    excerpt = models.CharField(max_length=200, null=True, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    fig = models.ImageField(verbose_name="feature photo of post", null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.now())
    edited_date = models.DateTimeField(default=datetime.now())

    def __str__(self) -> str:
        return self.title
