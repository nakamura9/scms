# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=128, null=True)
    memo = models.TextField()
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(default=timezone.now)
    amount = models.FloatField()
    credit = models.ForeignKey('accounting.Account', related_name="credit")
    debit = models.ForeignKey('accounting.Account')
    Journal = models.ForeignKey('accounting.Journal',null=True)
    #signal transactions 
    def __str__(self):
        if self.reference:
            return str(self.id) + " " + self.reference
        else:
            return str(self.id)

    def save(self, *args, **kwargs):
        super(Transaction, self).save(*args, **kwargs)
        # flawed, will result in erroneous transaction updates.
        self.credit.balance += self.amount
        self.credit.save()
        self.debit.balance -= self.amount
        self.debit.save()

#implement forms as wrappers for transactions

class Account(models.Model):
    name = models.CharField(max_length=64)
    balance = models.FloatField()
    type = models.CharField(max_length=32, choices=[
        ('expense', 'Expense'), 
        ('asset', 'Asset'), 
        ('liability', 'Liability')])
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def update_balance(self, **kwargs):
        print self.balance 
        print kwargs
        #self.save()

class Ledger(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name 


class Journal(models.Model):
    name = models.CharField(max_length=64)
    start_period = models.DateField()
    end_period = models.DateField()

    def __str__(self):
        return self.name 

class Tax(models.Model):
    name = models.CharField(max_length=64)
    rate = models.FloatField()

    def __str__(self):
        return self.name
    
class WorkBook(models.Model):
    name = models.CharField(max_length=64)
    #all adjustments are added to a workbook 

class Adjustmet(models.Model):
    id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey('accounting.Transaction')
    workbook = models.ForeignKey('accounting.WorkBook')
    description = models.TextField()
    # add fields for amounts adjusted etc

    