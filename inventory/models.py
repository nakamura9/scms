# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=64)
    contact_person = models.CharField(max_length=64, blank=True, null=True)
    physical_address = models.CharField(max_length=128, blank=True, null=True)
    telephone = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(max_length=64, blank=True, null=True)
    website = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    item_name = models.CharField(max_length = 32)
    code = models.AutoField(primary_key=True)
    unit = models.ForeignKey('inventory.UnitOfMeasure', blank=True, null=True)
    unit_sales_price = models.FloatField()
    unit_purchase_price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey("inventory.Supplier", blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    minimum_order_level = models.IntegerField( blank=True, null=True)
    maximum_stock_level = models.IntegerField( blank=True, null=True)
    category = models.ForeignKey('inventory.Category', blank=True, null=True)
    sub_category = models.ForeignKey('inventory.Category', related_name='sub_category', blank=True, null=True)

    def __str__(self):
        return str(self.code) + " - " + self.item_name

class Order(models.Model):
    expected_receipt_date = models.DateField()
    issue_date = models.DateField()
    supplier = models.ForeignKey('inventory.supplier', blank=True, null=True)
    bill_to = models.CharField(max_length=128, blank=True, null=True)
    ship_to = models.CharField(max_length=128, blank=True, null=True)
    tracking_number = models.CharField(max_length=64, blank=True, null=True)
    items = models.ManyToManyField('inventory.Item')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return 'Order:' + str(self.pk) + ' - ' + self.issue_date

class OrderItems(models.Model):
    item = models.ForeignKey('inventory.item')
    quantity = models.FloatField()
    order_price = models.FloatField()

    def __str__(self):
        return self.item + ' -' + str(self.order_price)

class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class StockReceipt(models.Model):
    order = models.ForeignKey('inventory.Order')
    receive_date = models.DateField()
    note =models.TextField( blank=True, null=True)
    fully_received = models.BooleanField()

    def __str__(self):
        return str(self.pk) + ' - ' + self.receive_date