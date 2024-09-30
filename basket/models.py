from django.db import models
from django.conf import settings
from cards.models import Product

class Basket(models.Model):
    """
    Represents a user's shopping basket.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Связываем корзину с пользователем
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        total = sum(item.product.price * item.quantity for item in self.items.all())
        return total

    def __str__(self):
        return f"Basket of {self.user.phone_number}"  # Отображение корзины по номеру телефона пользователя

class BasketItem(models.Model):
    """
    Represents an item in the shopping basket.
    """
    
    basket = models.ForeignKey(Basket, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"
