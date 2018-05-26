# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import models 
import os
from common_data.utilities import ExtraContext
import forms
from common_data.utilities import ExtraContext

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


class OrderCreateView(ExtraContext, CreateView):
    form_class = forms.OrderForm
    model = models.Order
    success_url = reverse_lazy('inventory:home')
    template_name = os.path.join("inventory", "order_create.html")
    extra_context = {"title": "Create New Purchase Order"}

class OrderUpdateView(ExtraContext, UpdateView):
    form_class = forms.OrderForm
    model = models.Order
    success_url = reverse_lazy('inventory:home')
    template_name = os.path.join("common_data", "create_template.html")
    extra_context = {"title": "Update Existing Purchase Order"}

class OrderListView(ExtraContext, ListView):
    paginate_by = 5
    model = models.Order
    template_name = os.path.join("inventory", "order_list.html")
    extra_context = {"title": "Order List",
                    "new_link": reverse_lazy("inventory:order-create")}