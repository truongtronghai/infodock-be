from django.db.models.signals import pre_save

from .models import Category


def make_slug_for_category(sender, **kwargs):
    category = kwargs["instance"]  # get the object triggering signal

    category.slug = (category.name).lower().replace(" ", "-")


pre_save.connect(make_slug_for_category, sender=Category)
