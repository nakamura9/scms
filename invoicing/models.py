# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from common_data.models import Person

# Create your models here.
class Customer(Person):
    billing_address = models.CharField(max_length =128, null= True)
    phone_two = models.CharField(max_length = 16, null = True)
    account_number = models.CharField(max_length= 16, null=True)
    other_details = models.TextField( null =True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Invoice(models.Model):
    customer = models.ForeignKey("invoicing.Customer")
    date = models.DateField()
    number = models.AutoField(primary_key = True)
    terms = models.CharField(max_length = 64)# give finite choices
    comments = models.TextField(null = True)
    paid_in_full = models.BooleanField(default=False)
    items = models.ManyToManyField("invoicing.InvoiceItem", null=True )
    account = models.ForeignKey("invoicing.Account")

    @property
    def total(self):
        total = 0
        for item in self.items.all():
            total += item.subtotal
        return total

    @property
    def balance_due(self):
        total_payments = 0
        for p in self.payment_set.all():
            total_payments += p.amount
        due = self.total - total_payments
        if due <= 0:
            self.paid_in_full = True
        return due

    def __str__(self):
        return str(self.pk)

class InvoiceItem(models.Model):
    item = models.ForeignKey("invoicing.Item")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.item.item_name + " * " + str(self.quantity)

    @property
    def subtotal(self):
        return self.quantity * self.item.unit_price

class Item(models.Model):
    item_name = models.CharField(max_length = 32)
    code = models.AutoField(primary_key=True)
    unit_price = models.FloatField()
    description = models.TextField()
    
    def __str__(self):
        return str(self.code) + " - " + self.item_name + " - " + \
            str(self.unit_price)

class SalesRep(Person):
    title = models.CharField(max_length=32, choices=[
        ("teller", "Teller"),
        ("admin", "Administrator")
    ])
    username = models.CharField(max_length =32)
    password = models.CharField(max_length=32)#fix this

    def __str__(self):
        return self.username 

class Payment(models.Model):
    #invoices need to be searchable by customer
    invoice = models.ForeignKey("invoicing.Invoice")
    amount = models.FloatField()
    date = models.DateField()
    method = models.CharField(max_length=32, choices=[("cash", "Cash" ),
                                        ("transfer", "Transfer"),
                                        ("debit card", "Debit Card"),
                                        ("ecocash", "EcoCash")])
    reference_number = models.AutoField(primary_key=True)
    #automatically populated by sales rep currently logged in
    sales_rep = models.ForeignKey("invoicing.SalesRep")
    account = models.ForeignKey("invoicing.Account")

    def __str__(self):
        return self.pk


class Account(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    balance =  models.FloatField()
    reps = models.ForeignKey("invoicing.SalesRep")

    def __str__(self):
        return self.name