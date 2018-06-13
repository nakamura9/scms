# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-07 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.CharField(choices=[('expense', 'Expense'), ('asset', 'Asset'), ('liability', 'Liability')], default='asset', max_length=32),
            preserve_default=False,
        ),
    ]