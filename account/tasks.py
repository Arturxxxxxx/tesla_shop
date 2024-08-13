# tasks.py
from celery import shared_task
from .utils import send_sms

@shared_task
def send_activation_code(activation_code, phone_number):
    message = f"Your activation code is: {activation_code}"
    response = send_sms(phone_number, message)
    return response
