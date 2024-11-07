from django.db import models
from cards.models import Product  # Импортируем Product из приложения cards
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class PaymentSession(models.Model):
    # Вместо Account из текущего приложения, используем модель Account из другого приложения
    account = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name="payment_sessions")  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Продукт из приложения cards
    session_id = models.CharField(max_length=100, unique=True)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Автоматический order_id
    valid_through = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentSession {self.session_id} for {self.account.user.username}"
