# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import os
from django.http import HttpResponseRedirect
from django.shortcuts import render
import forms
from models import Invoice, Quote
from accounting.models import Tax, Transaction,Journal,Account
from inventory.models import Item
from common_data.utilities import ExtraContext, apply_style,load_config
from rest_framework import generics, viewsets
from serializers import * 
import json
from django.urls import reverse_lazy
from django.conf import settings



############################################
#           API ViewSets                   #
############################################


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


class InvoiceItemAPIViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer


class QuoteAPIViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class QuoteItemAPIViewSet(viewsets.ModelViewSet):
    queryset = QuoteItem.objects.all()
    serializer_class = QuoteItemSerializer

#########################################
#           Class Based Views           #
#########################################
#simple forms that require no js
# item
# customr
# sales_rep


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
    extra_context = {"title": "List of Customers",
                    "new_link": reverse_lazy("invoicing:create-customer")}
    template_name = os.path.join("invoicing", "customer_list.html")
    model = Customer
    paginate_by = 2
    
    def get_queryset(self):
        return self.model.objects.all()

class PaymentCreateView(ExtraContext, CreateView):
    extra_context = {"title": "Create New Payment"}
    template_name = os.path.join("common_data", "create_template.html")
    model = Payment
    success_url = reverse_lazy("invoicing:home")
    form_class = forms.PaymentForm

    def post(self,request, *args, **kwargs):
        resp = super(PaymentCreateView, self).post(request, *args, **kwargs)
        p = Payment.objects.latest('pk')
        if request.POST.get('create_transaction', False):
            Transaction(
                date=p.date,
                amount = p.invoice.total,
                memo = "transaction concluded from payment number: " + str(p.pk),
                reference = "transaction concluded from payment number: " + str(p.pk),
                credit=Account.objects.get(name="Current Account"),
                debit=Account.objects.get(name="Accounts Receivable"),
                Journal=Journal.objects.first()# change this!
            ).save()

        return resp

class PaymentUpdateView(ExtraContext, UpdateView):
    extra_context = {"title": "Update Existing Payment"}
    template_name = os.path.join("common_data", "create_template.html")
    model = Payment
    form_class = forms.PaymentForm
    success_url = reverse_lazy("invoicing:home")


class PaymentListView(ExtraContext, ListView):
    extra_context = {"title": "List of Payments",
                    "new_link": reverse_lazy("invoicing:create-payment")}
    template_name = os.path.join("invoicing", "payment_list.html")
    model = Payment
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
    extra_context = {"title": "List of Sales Representatives",
                    "new_link": reverse_lazy("invoicing:create-sales-rep")}
    template_name = os.path.join("invoicing", "sales_rep_list.html")
    model = SalesRep
    paginate_by = 2
    
    def get_queryset(self):
        return self.model.objects.all()


class InvoiceListView(ExtraContext, ListView):
    extra_context = {"title": "Invoice List",
                    "new_link": reverse_lazy("invoicing:create-invoice")}
    template_name = os.path.join("invoicing", "invoice_list.html")
    model = Invoice
    paginate_by = 5
    
    def get_queryset(self):
        return self.model.objects.all()



class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = os.path.join("invoicing", "invoice_templates",
        'invoice.html')
    def get_context_data(self, *args, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(*args, **kwargs)
        context.update(load_config())
        context['title'] = 'Invoice'
        return apply_style(context)

        
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
        
        if request.POST.get('create_transaction', False):
            Transaction(
                date=inv.date,
                amount = inv.total,
                memo = "transaction concluded from invoice number: " + str(inv.pk),
                reference = "transaction concluded from invoice number: " + str(inv.pk),
                credit=Account.objects.get(name="Accounts Receivable"),
                debit=Account.objects.get(name="General Sales"),
                Journal=Journal.objects.first()# change this!
            ).save()
        
        return resp

class InvoiceUpdateView(ExtraContext, UpdateView):
    extra_content = {"title": "Update Invoice"}
    template_name = os.path.join("invoicing", "invoice_update.html")
    model = Invoice
    form_class = forms.InvoiceForm
    success_url = reverse_lazy("invoicing:home")

    def post(self, request, *args, **kwargs):
        # implement check for whether a transaction exists
        resp = super(InvoiceUpdateView, self).post(request, *args, **kwargs)
        inv = self.get_object()
        for item in request.POST.getlist("items[]"):
            pk, quantity = tuple(item.split("-"))
            inv.items.create(quantity=quantity,
                    item=Item.objects.get(pk=pk))
        for pk in request.POST.getlist("removed_items[]"):
            InvoiceItem.objects.get(pk=pk).delete()
        
        if request.POST.get('create_transaction', False):
            Transaction(
                date=inv.date,
                amount = inv.total,
                memo = "transaction concluded from invoice number: " + str(inv.pk),
                reference = "transaction concluded from invoice number: " + str(inv.pk),
                credit=Account.objects.get(name="Accounts Receivable"),
                debit=Account.objects.get(name="General Sales"),
                Journal=Journal.objects.first()# change this!
            ).save()

        return resp

class QuoteCreateView(ExtraContext, CreateView):
    extra_content = {"title": "Create a New Quote"}
    template_name = os.path.join("invoicing", "quote_create.html")
    model = Quote
    form_class = forms.QuoteForm
    success_url = reverse_lazy("invoicing:home")

    def post(self, request, *args, **kwargs):
        resp = super(QuoteCreateView, self).post(request, *args, **kwargs)
        quo = Quote.objects.latest("pk")
        for item in request.POST.getlist("items[]"):
            pk, quantity = tuple(item.split("-"))
            quo.items.create(quantity=quantity,
                    item=Item.objects.get(pk=pk))
        
        return resp

class QuoteUpdateView(ExtraContext, UpdateView):
    extra_content = {"title": "Update an existing Quotation"}
    template_name = os.path.join("invoicing", "quote_update.html")
    model = Quote
    form_class = forms.QuoteForm
    success_url = reverse_lazy("invoicing:home")

    def post(self, request, *args, **kwargs):
        resp = super(QuoteUpdateView, self).post(request, *args, **kwargs)
        quo = Quote.objects.latest("pk")
        # add update prices toggle for for each quote item item
        for item in request.POST.getlist("items[]"):
            pk, quantity = tuple(item.split("-"))
            quo.items.create(quantity=quantity,
                    item=Item.objects.get(pk=pk))

        for pk in request.POST.getlist("removed_items[]"):
            QuoteItem.objects.get(pk=pk).delete()
        
        return resp

class QuoteDetailView(DetailView):
    model = Quote
    template_name = os.path.join("invoicing", "quote_templates",
        'quote.html')
    
    def get_context_data(self, *args, **kwargs):
        context = super(QuoteDetailView, self).get_context_data(*args, **kwargs)
        context.update(load_config())
        context['title'] = 'Quotation'
        return apply_style(context)


class QuoteListView(ExtraContext, ListView):
    extra_context = {
        "title": "Quotation List",
        "new_link": reverse_lazy("invoicing:create-quote")
        }
    template_name = os.path.join("invoicing", "quote_list.html")
    model = Quote
    paginate_by = 5
    
    def get_queryset(self):
        return self.model.objects.all()

class ReceiptCreateView(ExtraContext, CreateView):
    extra_context = {
        'title': 'Create New Receipt'
    }
    template_name = os.path.join('common_data', 'create_template.html')
    form_class = forms.ReceiptForm
    model = Receipt
    success_url = reverse_lazy('invoicing:home')

    

class ReceiptListView(ExtraContext, ListView):
    extra_context = {
        "title": "List of Receipts",
        "new_link": reverse_lazy("invoicing:create-receipt")
        }
        
    template_name = os.path.join("invoicing", "receipt_list.html")
    model = Receipt
    paginate_by = 5
    
    def get_queryset(self):
        return self.model.objects.all()


class ReceiptDetailView(DetailView):
    model = Receipt
    template_name = os.path.join("invoicing", "receipt_templates",
        'receipt.html')
    
    def get_context_data(self, *args, **kwargs):
        context = super(ReceiptDetailView, self).get_context_data(*args, **kwargs)
        context.update(load_config())
        context['title'] = 'Receipt'
        return apply_style(context)


class ReceiptUpdateView(ExtraContext, UpdateView):
    extra_context = {
        'title': 'Update Existing Receipt'
    }
    template_name = os.path.join('common_data', 'create_template.html')
    form_class = forms.ReceiptForm
    model = Receipt
    success_url = reverse_lazy('invoicing:home')

#########################################################
#                  Template Views                       #
#########################################################

#views with forms augmented with react use template views


class ConfigView(FormView):
    template_name = os.path.join("invoicing", "config.html")
    form_class = forms.ConfigForm
    
    
    def get_context_data(self):
        
        context = super(ConfigView, self).get_context_data()
        context['logo']='/media/logo/' + load_config()['logo']
        context['taxes'] = Tax.objects.all()
        return context


    def get_initial(self):
        return load_config()

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if  request.FILES.get('logo', None):
            file = request.FILES['logo']
            filename = file.name
            print dir(file)
            path = os.path.join(settings.MEDIA_ROOT, 'logo', filename)
            data['logo'] = filename
            with open(path, 'wb+') as img:
                for chunk in file.chunks():
                    img.write(chunk)
        else:
            # keep the existing logo if no changes have been made
            data['logo'] = load_config()['logo']
            
        json.dump(data, open("config.json", 'w'))
        return HttpResponseRedirect(reverse_lazy("invoicing:home"))

class Home(TemplateView):
    template_name = os.path.join("invoicing", "home.html")


class InvoiceDeleteView(DeleteView):
    template_name = os.path.join("common_data", "delete_template.html")
    model = Invoice
    success_url = reverse_lazy("invoicing:invoices-list")

class PaymentDeleteView(DeleteView):
    template_name = os.path.join("common_data", "delete_template.html")
    model = Payment
    success_url = reverse_lazy("invoicing:invoices-list")


class QuoteDeleteView(DeleteView):
    template_name = os.path.join("common_data", "delete_template.html")
    model = Quote
    success_url = reverse_lazy("invoicing:quote-list")

class ReceiptDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    model = Receipt
    success_url = reverse_lazy('invoicing.receipt-list')

def create_invoice_from_quotation(request, pk):
    pass


def create_receipt_from_payment(request, pk):
    pass