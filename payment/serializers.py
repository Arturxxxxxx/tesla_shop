from rest_framework import serializers
from .models import PaymentSession, Order, OrderItem, Order
from cards.models import Product 


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    
    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    client_name = serializers.CharField(source='client.get_full_name')
    client_phone = serializers.CharField(source='client.phone_number')

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
            'items'
        ]

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']  # Указываем только необходимые для создания поля

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'client',
            'total_amount',
            'currency',
            'client_phone',
            'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # Убираем данные по товарам
        order = Order.objects.create(**validated_data)  # Создаем заказ

        # Создаем элементы заказа (товары)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
