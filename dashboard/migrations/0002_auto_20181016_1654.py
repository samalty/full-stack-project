# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-16 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='task1',
            field=models.CharField(max_length=200),
        ),
    ]