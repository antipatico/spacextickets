# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-15 14:28
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180605_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AddField(
            model_name='order',
            name='is_temporary',
            field=models.BooleanField(default=True, verbose_name='temporary_order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='booking_code',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='booking code'),
        ),
    ]