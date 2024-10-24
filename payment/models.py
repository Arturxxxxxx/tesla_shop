from django.conf import settings
from django.db import models

class Payment(models.Model):
    firls_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
