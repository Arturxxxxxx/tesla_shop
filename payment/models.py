# from django.db import models
# from django.contrib.auth import get_user_model
# from django.conf import settings

# User = get_user_model()

# class Account(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f"{self.user.username}'s Account"


# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name


# class PaymentSession(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="payment_sessions")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     session_id = models.CharField(max_length=100, unique=True)
#     valid_through = models.DateTimeField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.CharField(max_length=3)
#     order_id = models.CharField(max_length=100)
#     status = models.CharField(max_length=20, default="pending")  # 'pending', 'completed', 'failed'
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"PaymentSession {self.session_id} for {self.account.user.username}"
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Account"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PaymentSession(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="payment_sessions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Автоматический order_id
    valid_through = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentSession {self.session_id} for {self.account.user.username}"
