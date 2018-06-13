# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

from common_data.models import Person

# Create your models here.
class Customer(Person):
    billing_address = models.CharField(max_length =128, null= True)
    phone_two = models.CharField(max_length = 16, null = True)
    account_number = models.CharField(max_length= 16, null=True)
    other_details = models.TextField( null =True)

    def __str__(self):
        return self.first_name + " " + self.last_name

#add support for discounts
#add support for credit notes

class Invoice(models.Model):
    customer = models.ForeignKey("invoicing.Customer")
    date = models.DateField()
    number = models.AutoField(primary_key = True)
    terms = models.CharField(max_length = 64)# give finite choices
    comments = models.TextField(null = True)
    paid_in_full = models.BooleanField(default=False)
    tax = models.ForeignKey('accounting.Tax', null=True)
    salesperson = models.ForeignKey('invoicing.SalesRep', null=True)
    items = models.ManyToManyField("invoicing.InvoiceItem")
    account = models.ForeignKey("accounting.Account", null=True)
    status = models.CharField(max_length=16, choices=[
        ('draft', 'Draft'),
        ('sent', 'Sent')
    ])

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

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)
        #make sure updates dont do this again
        for item in items:
            item.item.quantity -= item.quantity

class InvoiceItem(models.Model):
    item = models.ForeignKey("inventory.Item")
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.item.item_name + " * " + str(self.quantity)

    @property
    def subtotal(self):
        return self.quantity * self.item.unit_sales_price

    def save(self, *args, **kwargs):
        super(InvoiceItem, self).save(*args, **kwargs)
        if not self.price:
            self.price = self.item.unit_sales_price
            self.save()

    def update_price(self):
        self.price = self.item.unit_sales_price
        self.save()


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
    account = models.ForeignKey("accounting.Account")

    def __str__(self):
        return str(self.pk)

    @property
    def due(self):
        return self.invoice.total - self.amount

class Quote(models.Model):
    date = models.DateField(default=datetime.date.today)
    customer = models.ForeignKey('invoicing.Customer')
    number = models.AutoField(primary_key = True)
    salesperson = models.ForeignKey('invoicing.SalesRep', null=True)
    comments = models.TextField(null = True)
    tax = models.ForeignKey('accounting.Tax', null=True)
    items = models.ManyToManyField("invoicing.QuoteItem")
    invoiced = models.BooleanField(default=False)
    
    @property
    def total(self):
        return reduce((lambda x,y: x + y), 
            [i.price * i.quantity for i in self.items.all()])

class QuoteItem(models.Model):
    item = models.ForeignKey('inventory.Item')
    quantity = models.IntegerField()
    price = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        super(QuoteItem, self).save(*args, **kwargs)
        if not self.price:
            self.price = self.item.unit_sales_price
            self.save()
    
    @property
    def subtotal(self):
        return self.price * self.quantity

    def update_price(self):
        self.price = self.item.unit_sales_price
        self.save()

class Receipt(models.Model):
    payment = models.ForeignKey('invoicing.Payment')
    comments = models.TextField()
    