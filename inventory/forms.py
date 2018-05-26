from django import forms
import models 
from common_data.forms import BootstrapMixin

#models ommitted UnitOfMeasure OrderItems Category

class SupplierForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = '__all__'
        model = models.Supplier
        
class ItemForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = '__all__'
        model = models.Item

class OrderForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = '__all__'
        model = models.Order
        widgets = {
            'items': forms.MultipleHiddenInput
        }
        
class StockReceiptForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = '__all__'
        model= models.StockReceipt
        widgets = {
            'order': forms.HiddenInput
        }


