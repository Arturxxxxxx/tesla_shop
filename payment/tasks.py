from celery import shared_task
import requests
from .models import Payment
from decouple import config 

BANK_AUTH_HASH = config('BANK_AUTH_HASH')


@shared_task
def check_payment_status(quid):
    payment = Payment.objects.get(quid=quid)
    response = requests.get(
        f"https://ibank2.cbk.kg/otp/status?quid={quid}",
        headers={
            "authenticate": BANK_AUTH_HASH,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    status_data = response.json()
    
    # Обновление статуса на основании ответа
    if status_data["code"] == 330:
        payment.status = "Успешен"
    elif status_data["code"] == 332:
        payment.status = "Неудача"
    payment.save()