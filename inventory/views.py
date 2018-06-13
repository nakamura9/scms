# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import models 
from accounting.models import Account, Transaction, Journal
import os
from common_data.utilities import ExtraContext
import forms
from common_data.utilities import ExtraContext
import serializers
from rest_framework.viewsets import ModelViewSet
from common_data.utilities import load_config, apply_style

class InventoryHome(ExtraContext, ListView):
    extra_context = {
        "title": "Inventory Home",
        "new_link": reverse_lazy("inventory:item-create")
        }
    paginate_by = 20
    model = models.Item
    template_name = os.path.join("inventory", "inventory_list.html")

#####################################################
#               Static Form Pages                   #
#####################################################

class SupplierCreateView(ExtraContext, CreateView):
    form_class = forms.SupplierForm
    model = models.Supplier
    success_url = reverse_lazy('inventory:home')
    template_name = os.path.join("common_data", "create_template.html")
    extra_context = {"title": "Create New Supplier"}

class SupplierUpdateView(ExtraContext, UpdateView):
    form_class = forms.SupplierForm
    model = models.Supplier
    success_url = reverse_lazy('inventory:home')
    template_name = os.path.join("common_data", "create_template.html")
    extra_context = {"title": "Update Existing Supplier"}

class SupplierListView(ExtraContext, ListView):
    paginate_by = 5
    model = models.Supplier
    template_name = os.path.join("inventory", "supplier_list.html")
    extra_context = {"title": "Supplier List",
                    "new_link": reverse_lazy("inventory:supplier-create")}

class ItemListView(ExtraContext, ListView):
    paginate_by = 3
    model = models.Item
    template_name = os.path.join('inventory', 'item_list.html')
    extra_context = {
        'title': 'Item List',
        "new_link": reverse_lazy("inventory:item-create")
    }

class ItemCreateView(ExtraContext, CreateView):
    form_class = forms.ItemForm
    model = models.Item
    success_url = reverse_lazy('inventory:home')
    template_name = os.path.join("common_data", "create_template.html")
    extra_context = {"title": "Create New Item"}

class ItemUpdateView(ExtraContext, UpdateView):
    form_class = forms.ItemForm
    model = models.Item
    success_url = reverse_lazy('inventory:home')
    template_name = os.path.join("common_data", "create_template.html")
    extra_context = {"title": "Update Existing Item"}

class ItemDetailView(DetailView):
    model = models.Item
    template_name = os.path.join("inventory", "item_detail.html")
    

class OrderCreateView(ExtraContext, CreateView):
    form_class = forms.OrderForm
    model = models.Order
    success_url = reverse_lazy('inventory:home')
    template_name = os.path.join("inventory", "order_create.html")
    extra_context = {"title": "Create New Purchase Order"}

    def post(self, request, *args, **kwargs):
        resp = super(OrderCreateView, self).post(request, *args, **kwargs)
        items = request.POST.getlist("items[]")
        order = models.Order.objects.latest('pk')
        
        for item in items:
            print item
            pk, price, quantity = item.split('-')
            order.items.create(item=models.Item.objects.get(pk=pk),
                                quantity=quantity,
                                order_price=price)

        #determine accounts based on order status
        debit = None
        credit = None
        if order.status == 'draft':
            pass
        elif order.status == 'submitted':
            debit = Account.objects.get(name='Current Account')
            credit = Account.objects.get(name='Accounts Receivable')
        else: # received
            debit = Account.objects.get(name='Accounts Receivable')
            credit = Account.objects.get(name='Inventory')
        
        if request.POST.get('create_transaction', False) and debit:
            Transaction(
                date=order.issue_date,
                amount = order.total,
                memo = "transaction derived from order number: " + str(order.pk),
                reference = "transaction derived from order number: " + str(order.pk),
                credit=credit,
                debit=debit,
                Journal=Journal.objects.first()# change this!
            ).save()            

        return resp
        
class OrderUpdateView(ExtraContext, UpdateView):
    form_class = forms.OrderForm
    model = models.Order
    success_url = reverse_lazy('inventory:home')
    template_name = os.path.join("inventory", "order_update.html")
    extra_context = {"title": "Update Existing Purchase Order"}

    def post(self, request, *args, **kwargs):
        resp = super(OrderUpdateView, self).post(request, *args, **kwargs)
        items = request.POST.getlist("items[]")
        order = self.get_object()

        for item in items:
            print item
            pk, price, quantity = item.split('-')
            order.items.create(item=models.Item.objects.get(pk=pk),
                                quantity=quantity,
                                order_price=price)

        for data in request.POST.getlist("removed_items[]"):
            pk, name = data.split('-')
            models.OrderItems.objects.get(pk=pk).delete()
        return resp


class OrderListView(ExtraContext, ListView):
    paginate_by = 5
    model = models.Order
    template_name = os.path.join("inventory", "order_list.html")
    extra_context = {"title": "Order List",
                    "new_link": reverse_lazy("inventory:order-create")}

class OrderDeleteView(DeleteView):
    model = models.Order
    template_name = os.path.join('common_data', 'delete_template.html')
    success_url = reverse_lazy('inventory:order-list')


class OrderDetailView(ExtraContext, DetailView):
    model = models.Order
    template_name = os.path.join('inventory', 'order_templates', 'order.html')
    extra_context = {
        'title': 'Purchase Order',
    }

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args, **kwargs)
        context.update(load_config())
        return apply_style(context)


class StockReceiptCreateView(CreateView):
    form_class = forms.StockReceiptForm
    model = models.StockReceipt
    success_url = reverse_lazy('inventory:home')
    template_name = os.path.join("common_data", "create_template.html")
    extra_context = {"title": "Receive Ordered goods"}

class ItemAPIView(ModelViewSet):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer

class OrderAPIView(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

class OrderItemAPIView(ModelViewSet):
    queryset = models.OrderItems.objects.all()
    serializer_class = serializers.OrderItemSerializer

class ItemDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    model = models.Item
    success_url = reverse_lazy('invoicing.item-list')
