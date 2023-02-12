# Generated by Django 4.1.6 on 2023-02-12 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='follow_user',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user',
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
