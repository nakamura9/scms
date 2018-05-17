from __future__ import unicode_literals

from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length =32)
    last_name = models.CharField(max_length =32)
    address = models.CharField(max_length =128)
    email = models.CharField(max_length =32)
    phone = models.CharField(max_length =16)

    class Meta:
        abstract = True