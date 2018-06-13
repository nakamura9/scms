from django import forms
from common_data.forms import BootstrapMixin
import models

class TransactionForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields="__all__"
        model = models.Transaction


class AccountForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields="__all__"
        model = models.Account

class LedgerForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields="__all__"
        model = models.Ledger


class JournalForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields="__all__"
        model = models.Journal