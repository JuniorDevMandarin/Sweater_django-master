# Generated by Django 4.0.5 on 2022-08-30 19:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0002_alter_social_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='social',
            name='likes',
            field=models.ManyToManyField(related_name='blog_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]