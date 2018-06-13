from rest_framework import serializers
from models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False)
    class Meta:
        fields = "__all__"
        model = OrderItems

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = "__all__"