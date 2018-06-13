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
    create_transaction = forms.BooleanField(initial=True, required=False)
    
    class Meta:
        exclude = ["items"]
        model = models.Order
        
        
class StockReceiptForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        exclude = 'received_items',
        model= models.StockReceipt
        


