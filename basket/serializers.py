from rest_framework import serializers
from .models import Cart, CartItem
from cards.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'get_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'get_total_price']

    def get_total_price(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())
