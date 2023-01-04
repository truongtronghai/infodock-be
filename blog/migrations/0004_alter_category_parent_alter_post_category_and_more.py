# Generated by Django 4.0 on 2023-01-04 09:08

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_category_parent_alter_post_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="blog.category",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="posts_in_category",
                to="blog.category",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="created_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 1, 4, 16, 8, 27, 247980)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="edited_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 1, 4, 16, 8, 27, 247991)
            ),
        ),
    ]
