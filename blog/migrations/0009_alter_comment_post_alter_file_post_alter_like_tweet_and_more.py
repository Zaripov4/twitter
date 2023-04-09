# Generated by Django 4.1.6 on 2023-03-17 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0008_resetcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="blog.post",
            ),
        ),
        migrations.AlterField(
            model_name="file",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="blog.post"
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="tweet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="blog.post"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="blog.post",
            ),
        ),
    ]
