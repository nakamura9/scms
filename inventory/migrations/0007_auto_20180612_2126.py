# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-12 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20180612_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockreceipt',
            name='received_items',
            field=models.ManyToManyField(null=True, to='inventory.OrderItems'),
        ),
    ]
