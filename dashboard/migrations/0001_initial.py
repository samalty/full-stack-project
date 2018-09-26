# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-24 10:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('fee', models.IntegerField()),
                ('launched', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('deadline', models.DateField(blank=True)),
                ('project_status', models.CharField(choices=[('Done', 'Done'), ('Doing', 'Doing'), ('To Do', 'To Do')], max_length=5)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('High', 'High'), ('Medium', 'Medium')], max_length=6)),
                ('task1', models.CharField(blank=True, max_length=200)),
                ('task1_status', models.CharField(choices=[('Done', 'Done'), ('Doing', 'Doing'), ('To Do', 'To Do')], default='To Do', max_length=5)),
                ('task2', models.CharField(blank=True, max_length=200)),
                ('task2_status', models.CharField(choices=[('Done', 'Done'), ('Doing', 'Doing'), ('To Do', 'To Do')], default='To Do', max_length=5)),
                ('task3', models.CharField(blank=True, max_length=200)),
                ('task3_status', models.CharField(choices=[('Done', 'Done'), ('Doing', 'Doing'), ('To Do', 'To Do')], default='To Do', max_length=5)),
                ('task4', models.CharField(blank=True, max_length=200)),
                ('task4_status', models.CharField(choices=[('Done', 'Done'), ('Doing', 'Doing'), ('To Do', 'To Do')], default='To Do', max_length=5)),
                ('task5', models.CharField(blank=True, max_length=200)),
                ('task5_status', models.CharField(choices=[('Done', 'Done'), ('Doing', 'Doing'), ('To Do', 'To Do')], default='To Do', max_length=5)),
                ('signed_off', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
