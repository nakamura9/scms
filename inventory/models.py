# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from invoicing.models import Invoice, InvoiceItem


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
    image = models.FileField(blank=True, null=True, upload_to=settings.MEDIA_ROOT)
    quantity = models.FloatField(blank=True, default=0)
    minimum_order_level = models.IntegerField( blank=True, default=0)
    maximum_stock_level = models.IntegerField( blank=True, default=0)
    category = models.ForeignKey('inventory.Category', blank=True, null=True)
    sub_category = models.ForeignKey('inventory.Category', related_name='sub_category', blank=True, null=True)

    def __str__(self):
        return str(self.code) + " - " + self.item_name

    @property
    def stock_value(self):
        return self.unit_sales_price * self.quantity
        
    @property
    def sales_to_date(self):
        items = InvoiceItem.objects.filter(item=self)
        total_sales = reduce(lambda x,y: x + y, [item.quantity * item.price for item in items], 0)
        return total_sales
    
class Order(models.Model):
    expected_receipt_date = models.DateField()
    issue_date = models.DateField()
    supplier = models.ForeignKey('inventory.supplier', blank=True, null=True)
    bill_to = models.CharField(max_length=128, blank=True, null=True)
    ship_to = models.CharField(max_length=128, blank=True, null=True)
    tracking_number = models.CharField(max_length=64, blank=True, null=True)
    items = models.ManyToManyField('inventory.OrderItems')
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=16, choices=[
        ('received', 'Received'),
        ('draft', 'Draft'),
        ('submitted', 'Submitted')
    ])
    
    def __str__(self):
        return 'Order:' + str(self.pk) + ' - ' + str(self.issue_date)

    @property
    def total(self):
        return reduce(lambda x, y: x + y , [item.subtotal for item in self.items.all()], 0)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        if self.status == 'received':
            for item in self.items:
                item.item.quantity += item.quantity
                

class OrderItems(models.Model):
    item = models.ForeignKey('inventory.item')
    quantity = models.FloatField()
    #change and move this to the item
    #make changes to the react app as well
    order_price = models.FloatField()

    def __str__(self):
        return str(self.item) + ' -' + str(self.order_price)

    def save(self, *args, **kwargs):
        super(OrderItems, self).save(*args, **kwargs)
        if not self.order_price:
            self.order_price = self.item.unit_purchase_price

    @property
    def subtotal(self):
        return self.quantity * self.order_price

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
    received_items = models.ManyToManyField('inventory.OrderItems', null=True)
    fully_received = models.BooleanField()

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.receive_date)

    def save(self, *args, **kwargs):
        super(StockReceipt, self).save(*args, **kwargs)
        self.order.status = 'received'
        self.order.save()