from django import forms
from common_data.forms import BootstrapMixin
import models
from django.forms.widgets import HiddenInput, MultipleHiddenInput

class CustomerForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = '__all__'
        model = models.Customer
        fields_required = ['first_name', 'last_name']

class ItemForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = '__all__' 
        model = models.Item


class SalesRepForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = '__all__'
        model = models.SalesRep

class PaymentForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = '__all__'
        model = models.Payment

class AccountForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = '__all__'
        model = models.Account

class InvoiceForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = ["date","customer", "account", "paid_in_full", "terms", "comments"]
        widgets = {
            "customer": HiddenInput,
        }
        model = models.Invoice

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields["date"].widget.attrs["class"] = "form-control ui-date-picker"