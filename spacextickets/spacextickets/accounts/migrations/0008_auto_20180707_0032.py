# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-06 22:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20180606_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traveler',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.BaseUser', verbose_name='user'),
        ),
    ]