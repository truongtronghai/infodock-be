from django.db.models.signals import pre_save

from .models import Category, Post


def make_slug_for_category(sender, **kwargs):
    category = kwargs["instance"]  # get the object triggering signal
    if category.slug is None:
        category.slug = (category.name).lower().replace(" ", "-")


def make_slug_for_post(sender, **kwargs):
    post = kwargs["instance"]  # get the object triggering signal
    if post.slug is None:
        post.slug = (post.title).lower().replace(" ", "-")


pre_save.connect(make_slug_for_category, sender=Category)
pre_save.connect(make_slug_for_post, sender=Post)
