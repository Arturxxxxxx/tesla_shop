from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем корзину только текущего пользователя
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Проверка, есть ли у пользователя корзина
        cart, created = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

    def update(self, request, *args, **kwargs):
        cart = self.get_queryset().first()
        if not cart:
            return Response({'error': 'Корзина не найдена'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем товары корзины текущего пользователя
        cart = get_object_or_404(Cart, user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart = get_object_or_404(Cart, user=self.request.user)
        serializer.save(cart=cart)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
