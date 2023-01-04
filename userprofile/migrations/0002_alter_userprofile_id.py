# Generated by Django 4.0 on 2022-12-31 04:06

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False, unique=True
            ),
        ),
    ]