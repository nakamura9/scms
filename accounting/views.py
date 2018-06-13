# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import os
import serializers
from rest_framework import viewsets
import models 
import forms
from django.db.models import Q
from django.urls import reverse_lazy
from common_data.utilities import ExtraContext

class Dashboard(TemplateView):
    template_name = os.path.join('accounting', 'dashboard.html')

class TaxViewset(viewsets.ModelViewSet):
    queryset = models.Tax.objects.all()
    serializer_class = serializers.TaxSerializer

class TransactionCreateView(ExtraContext, CreateView):
    template_name = os.path.join('common_data', 'create_template.html')
    model = models.Transaction
    form_class = forms.TransactionForm
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {"title": "Create New Transaction"}

class TransactionDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    model = models.Transaction
    success_url = reverse_lazy('accounting:dashboard')

class TransactionUpdateView(ExtraContext, UpdateView):
    template_name = os.path.join('common_data', 'create_template.html')
    model = models.Transaction
    form_class = forms.TransactionForm
    success_url = reverse_lazy('accounting:dashboard')

class AccountCreateView(ExtraContext, CreateView):
    template_name = os.path.join('common_data', 'create_template.html')
    model = models.Account
    form_class = forms.AccountForm
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {"title": "Create New Account"}

class AccountUpdateView(ExtraContext, UpdateView):
    template_name = os.path.join('common_data', 'create_template.html')
    model = models.Account
    form_class = forms.AccountForm
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {"title": "Update Existing Account"}


class AccountDetailView(DetailView):
    template_name = os.path.join('accounting', 'account_detail.html')
    model = models.Account 

    def get_context_data(self, *args, **kwargs):
        #implemented because related manager not getting all transactions 
        context = super(AccountDetailView, self).get_context_data(*args, **kwargs)
        context['transactions'] = models.Transaction.objects.filter(
            Q(credit=self.object) | Q(debit=self.object))
        return context

class AccountListView(ExtraContext, ListView):
    template_name = os.path.join('accounting', 'account_list.html')
    model = models.Account
    paginate_by = 10
    extra_context = {
        "title": "Chart of Accounts",
        'new_link': reverse_lazy('accounting:create-account')
                }

class JournalCreateView(ExtraContext, CreateView):
    template_name = os.path.join('common_data', 'create_template.html')
    model = models.Journal
    form_class = forms.JournalForm
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {"title": "Create New Journal"}

class JournalDetailView(DetailView):
    template_name = os.path.join('accounting', 'journal_detail.html')
    model = models.Journal

class JournalListView(ExtraContext, ListView):
    template_name = os.path.join('accounting', 'journal_list.html')
    model = models.Journal
    paginate_by = 10
    extra_context = {
        "title": "Accounting Journals",
        'new_link': reverse_lazy('accounting:create-journal')
                }

