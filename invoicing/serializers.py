from rest_framework import serializers

from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


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

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

    
class InvoiceItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
        model = InvoiceItem
        fields = "__all__"

class InvoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Invoice
        fields = "__all__"