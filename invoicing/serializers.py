from rest_framework import serializers

from .models import *
from inventory.serializers import ItemSerializer

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class SalesRepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRep
        fields = "__all__"
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


    
class InvoiceItemSerializer(serializers.ModelSerializer):
    
    item = ItemSerializer(many=False)

    class Meta:
        model = InvoiceItem
        fields = ("id", "quantity", "item")

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    customer = CustomerSerializer(many=False)
    class Meta:
        model = Invoice
        fields = "__all__"

class QuoteItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False)
    class Meta:
        model = QuoteItem
        fields = "__all__"

class QuoteSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True)
    customer = CustomerSerializer(many=False)
    class Meta:
        model = Quote
        fields = "__all__"