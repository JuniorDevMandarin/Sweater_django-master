# Generated by Django 4.0.5 on 2022-09-01 16:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0004_alter_social_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
