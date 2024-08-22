# tasks.py
from celery import shared_task
from .utils import send_sms

@shared_task
def send_activation_code(verification_code, phone_number):
    # message = f"Your activation code is: {activation_code}"
    message = 'print'
    response = send_sms(phone_number, verification_code)
    return response
# @shared_task
# def send_activation_code(code, phone_number):
#     response = send_sms(phone_number, code)
#     print(code)
#     if not code:
#         print("Error: No verification code provided.")
#     else:
#         print(f"Sending activation code {code} to {phone_number}")
        # Логика отправки SMS с активационным кодом
        # Например, интеграция с SMS API