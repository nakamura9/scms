# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-14 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='description',
            field=models.TextField(),
        ),
    ]
