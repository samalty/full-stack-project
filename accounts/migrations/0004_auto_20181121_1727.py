# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-21 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20181120_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='profile_img/anon.png', upload_to='profile_img'),
        ),
    ]
