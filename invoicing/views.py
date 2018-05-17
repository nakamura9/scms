# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import os
from django.shortcuts import render
import forms
from models import Invoice, Item
from common_data.utilities import ExtraContext
from rest_framework import generics, viewsets
from serializers import * 
from django.urls import reverse_lazy

############################################
#           API ViewSets                   #
############################################

class ItemAPIViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class InvoiceAPIViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    

class CustomerAPIViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class PaymentAPIViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentsSerializer


class SalesRepsAPIViewSet(viewsets.ModelViewSet):
    queryset = SalesRep.objects.all()
    serializer_class = SalesRepsSerializer


class AccountAPIViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

#########################################
#           Class Based Views           #
#########################################
#simple forms that require no js
# item
# customr
# sales_rep
class ItemCreateView(ExtraContext, CreateView):
    extra_context = {"title": "Create New Item"}
    template_name = os.path.join("common_data", "create_template.html")
    model = Item
    success_url = reverse_lazy("invoicing:home")
    form_class = forms.ItemForm


class ItemUpdateView(ExtraContext, UpdateView):
    extra_context = {"title": "Update Existing Item"}
    template_name = os.path.join("common_data", "create_template.html")
    model = Item
    form_class = forms.ItemForm
    success_url = reverse_lazy("invoicing:home")


class ItemListView(ExtraContext, ListView):
    extra_context = {"title": "Item List"}
    template_name = os.path.join("common_data", "item_list.html")
    model = Item
    paginate_by = 2
    
    def get_queryset(self):
        return self.model.objects.all()


class CustomerCreateView(ExtraContext, CreateView):
    extra_context = {"title": "Create New Customer"}
    template_name = os.path.join("common_data", "create_template.html")
    model = Customer
    success_url = reverse_lazy("invoicing:home")
    form_class = forms.CustomerForm


class CustomerUpdateView(ExtraContext, UpdateView):
    extra_context = {"title": "Update Existing Customer"}
    template_name = os.path.join("common_data", "create_template.html")
    model = Customer
    form_class = forms.CustomerForm
    success_url = reverse_lazy("invoicing:home")


class CustomerListView(ExtraContext, ListView):
    extra_context = {"title": "List of Customers"}
    template_name = os.path.join("invoicing", "customer_list.html")
    model = Customer
    paginate_by = 2
    
    def get_queryset(self):
        return self.model.objects.all()


class SalesRepCreateView(ExtraContext, CreateView):
    extra_context = {"title": "Add New Sales Rep."}
    template_name = os.path.join("common_data", "create_template.html")
    model = SalesRep
    success_url = reverse_lazy("invoicing:home")
    form_class = forms.SalesRepForm


class SalesRepUpdateView(ExtraContext, UpdateView):
    extra_context = {"title": "Update Existing Sales Rep."}
    template_name = os.path.join("common_data", "create_template.html")
    model = SalesRep
    form_class = forms.SalesRepForm
    success_url = reverse_lazy("invoicing:home")


class SalesRepListView(ExtraContext, ListView):
    extra_context = {"title": "List of Sales Representatives"}
    template_name = os.path.join("invoicing", "sales_rep_list.html")
    model = SalesRep
    paginate_by = 2
    
    def get_queryset(self):
        return self.model.objects.all()


class InvoiceListView(ExtraContext, ListView):
    extra_context = {"title": "List of Invoices"}
    template_name = os.path.join("invoicing", "invoice_list.html")
    model = Invoice
    paginate_by = 5
    
    def get_queryset(self):
        return self.model.objects.all()


class InvoiceCreateView(ExtraContext, CreateView):
    extra_content = {"title": "Create a New Invoice"}
    template_name = os.path.join("invoicing", "invoice_create.html")
    model = Invoice
    form_class = forms.InvoiceForm
    success_url = reverse_lazy("invoicing:home")

    def post(self, request, *args, **kwargs):
        resp = super(InvoiceCreateView, self).post(request, *args, **kwargs)
        inv = Invoice.objects.latest("pk")
        for item in request.POST.getlist("items[]"):
            pk, quantity = tuple(item.split("-"))
            inv.items.create(quantity=quantity,
                    item=Item.objects.get(pk=pk))
        
        return resp

class InvoiceUpdateView(ExtraContext, UpdateView):
    extra_content = {"title": "Update Invoice"}
    template_name = os.path.join("invoicing", "invoice_update.html")
    model = Invoice
    form_class = forms.InvoiceForm
    success_url = reverse_lazy("invoicing:home")

#########################################################
#                  Template Views                       #
#########################################################

#views with forms augmented with react use template views




class Home(TemplateView):
    template_name = os.path.join("invoicing", "home.html")