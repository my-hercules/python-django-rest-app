# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 13:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employer', '0007_auto_20170924_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eorder',
            name='rec',
        ),
        migrations.AddField(
            model_name='eorder',
            name='rec',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pk', to=settings.AUTH_USER_MODEL),
        ),
    ]
