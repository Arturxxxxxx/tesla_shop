from django.db import models
from cards.models import Product  # Импортируем Product из приложения cards
from django.contrib.auth import get_user_model
from account.models import CustomUser
from django.utils import timezone
import uuid

User = get_user_model()

class PaymentSession(models.Model):
    # Вместо Account из текущего приложения, используем модель Account из другого приложения
    account = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name="payment_sessions")  
    products = models.ManyToManyField(Product, related_name='payment_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    order_id = models.CharField(max_length=50, unique=True)  # Автоматический order_id
    valid_through = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentSession {self.session_id} for {self.account.user.username}"

class OrderHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="order_history")
    products = models.ManyToManyField(Product)
    order_id = models.CharField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="completed")
    order_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.order_id} for {self.user.username}"
    




class Payment(models.Model):
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # Сумма в минорных единицах (например, тыйыны)
    quid = models.CharField(max_length=255, unique=True)
    txn_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Другие поля по необходимости
