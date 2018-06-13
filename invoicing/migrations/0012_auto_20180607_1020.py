# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-07 08:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0011_auto_20180523_2319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='reps',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='account',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='account',
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Item'),
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
