from rest_framework import serializers
from .models import PaymentSession, Order, OrderItem
from cards.models import Product 


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price']  # Поля продукта

class PaymentSessionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    client_name = serializers.CharField(source='account.get_full_name', read_only=True)
    client_phone = serializers.CharField(source='account.phone_number', read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = PaymentSession
        fields = [
            'order_id', 'created_at', 'products', 'client_name',
            'client_phone', 'client_address', 'status', 'total_cost'
        ]

    def get_total_cost(self, obj):
        return sum(product.price for product in obj.products.all())



    def get_client_name(self, ojb):
        return f"{ojb.account.last_name} {ojb.account.first_name}"
    

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    
    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    client_name = serializers.CharField(source='client.get_full_name')
    client_phone = serializers.CharField(source='client.phone_number')
    client_address = serializers.CharField(source='client.address')

    class Meta:
        model = Order
        fields = [
            'order_id',
            'order_date',
            'total_amount',
            'currency',
            'status',
            'client_name',
            'client_phone',
            'client_address',
            'items'
        ]