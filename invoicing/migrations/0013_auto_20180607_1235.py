# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-07 10:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
        ('invoicing', '0012_auto_20180607_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounting.Account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounting.Account'),
            preserve_default=False,
        ),
    ]
