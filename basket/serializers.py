from rest_framework import serializers
from .models import Cart, CartItem
from cards.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)  # Отображение продукта в строковом виде
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    total_price = serializers.SerializerMethodField()  # Поле для вычисления общей цены

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()  # Используем метод модели CartItem для получения цены


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)  # Вывод всех элементов корзины
    total_price = serializers.SerializerMethodField()  # Поле для общей суммы корзины

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())  # Общая сумма всех элементов корзины
