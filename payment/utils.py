# import requests
# from django.urls import reverse
# from .models import PaymentSession
# from decouple import config

# PAYLER_API_KEY = config('PAYLER_KEY')
# PAYLER_HOST = config('PAYLER_HOST')

# def create_payment_session(account, product):
#     """
#     Создаёт платёжную сессию с Payler для указанного аккаунта и продукта.
#     """
#     url = f"https://{PAYLER_HOST}/gapi/StartSession"
#     data = {
#         "key": PAYLER_API_KEY,
#         "type": "OneStep",
#         "order_id": f"order_{account.user.id}_{product.id}",
#         "amount": int(product.price * 100),  # Payler требует сумму в минимальных единицах (копейках)
#         "currency": "RUB",
#         "product": product.name,
#         "return_url_success": "https://yourdomain.com/success",
#         "return_url_decline": "https://yourdomain.com/decline",
#     }
#     response = requests.post(url, data=data)
#     response_data = response.json()
    
#     if response_data.get("session_id"):
#         payment_session = PaymentSession.objects.create(
#             account=account,
#             product=product,
#             session_id=response_data["session_id"],
#             order_id=data["order_id"],
#             status="pending",
#         )
#         return payment_session
#     else:
#         raise Exception("Failed to create payment session")

# def check_payment_status(session_id):
#     """
#     Проверяет статус платежа по session_id.
#     """
#     url = f"https://{PAYLER_HOST}/gapi/GetStatus"
#     data = {
#         "key": PAYLER_API_KEY,
#         "session_id": session_id
#     }
#     response = requests.post(url, data=data)
#     response_data = response.json()
    
#     if response_data.get("status") == "Completed":
#         payment_session = PaymentSession.objects.get(session_id=session_id)
#         payment_session.status = "completed"
#         payment_session.save()
#         return "completed"
#     elif response_data.get("status") == "Declined":
#         payment_session = PaymentSession.objects.get(session_id=session_id)
#         payment_session.status = "failed"
#         payment_session.save()
#         return "failed"
#     else:
#         return "pending"

# import requests
# import logging
# from .models import PaymentSession
# from decouple import config
# from datetime import datetime, timedelta

# PAYLER_API_KEY = config('PAYLER_KEY')
# PAYLER_HOST = config('PAYLER_HOST')

# # Настройка логирования
# logger = logging.getLogger(__name__)

# def create_payment_session(account, product):
#     """
#     Создает платежную сессию с Payler и настраивает 3DS, если это необходимо.
#     """
#     url = f"https://{PAYLER_HOST}/gapi/StartSession"
#     order_id = f"order_{account.user.id}_{product.id}"
#     data = {
#         "key": PAYLER_API_KEY,
#         "type": "OneStep",
#         "order_id": order_id,
#         "amount": int(product.price * 100),  # Payler требует сумму в минимальных единицах
#         "currency": "RUB",
#         "product": product.name,
#         "return_url_success": "https://yourdomain.com/success",
#         "return_url_decline": "https://yourdomain.com/decline",
#     }

#     response = requests.post(url, data=data)
#     response_data = response.json()
    
#     # Логирование запроса и ответа
#     logger.info(f"Отправлен запрос на {url} с данными: {data}")
#     logger.info(f"Получен ответ: {response_data}")

#     if response_data.get("session_id"):
#         # Проверка, требуется ли 3DS аутентификация
#         if "acs_url" in response_data:
#             logger.info("Требуется аутентификация 3DS.")
#             payment_session = PaymentSession.objects.create(
#                 account=account,
#                 product=product,
#                 session_id=response_data["session_id"],
#                 order_id=order_id,
#                 amount=product.price,
#                 currency="RUB",
#                 status="pending",
#             )
#             return payment_session, response_data["acs_url"], response_data.get("pareq")
#         else:
#             payment_session = PaymentSession.objects.create(
#                 account=account,
#                 product=product,
#                 session_id=response_data["session_id"],
#                 order_id=order_id,
#                 amount=product.price,
#                 currency="RUB",
#                 status="pending",
#             )
#             return payment_session, None, None
#     else:
#         error_message = "Не удалось создать платежную сессию"
#         logger.error(error_message)
#         raise Exception(error_message)


# def check_payment_status(session_id):
#     """
#     Проверяет статус платежа по session_id.
#     """
#     url = f"https://{PAYLER_HOST}/gapi/GetStatus"
#     data = {
#         "key": PAYLER_API_KEY,
#         "session_id": session_id
#     }
#     response = requests.post(url, data=data)
#     response_data = response.json()

#     logger.info(f"Проверка статуса платежа для session_id={session_id}")
#     logger.info(f"Получен ответ: {response_data}")

#     payment_session = PaymentSession.objects.get(session_id=session_id)
#     if response_data.get("status") == "Completed":
#         payment_session.status = "completed"
#     elif response_data.get("status") == "Declined":
#         payment_session.status = "failed"
#     else:
#         payment_session.status = "pending"
#     payment_session.save()

#     return payment_session.status


import requests
from django.utils.crypto import get_random_string
from django.utils import timezone
from .models import PaymentSession
from decouple import config
import logging

PAYLER_API_KEY = config('PAYLER_KEY')
PAYLER_HOST = config('PAYLER_HOST')

# Логирование
logger = logging.getLogger(__name__)

def generate_order_id():
    """Генерирует уникальный order_id для каждого платежа."""
    return f"order_{get_random_string(12)}"

# def create_payment_session(account, product):

    
#     """
#     Создаёт платёжную сессию с Payler для указанного аккаунта и продукта.
#     """
#     order_id = generate_order_id()
#     url = f"https://{PAYLER_HOST}/gapi/StartSession"
#     data = {
#         "key": PAYLER_API_KEY,
#         "type": "OneStep",
#         "order_id": order_id,
#         "amount": int(product.price * 100),  # Payler требует сумму в минимальных единицах (копейках)
#         "currency": "RUB",
#         "product": product.name,
#         "return_url_success": "https://koreacenter.kg/success",
#         "return_url_decline": "https://koreacenter.kg/decline",
#     }
#     response = requests.post(url, data=data)
#     response_data = response.json()
    
#     # Логирование ответа
#     logger.info(f"Ответ от Payler для создания сессии: {response_data}")

#     if response_data.get("session_id"):
#         payment_session = PaymentSession.objects.create(
#             account=account,
#             product=product,
#             session_id=response_data["session_id"],
#             order_id=order_id,
#             status="pending",
#             valid_through=timezone.now() + timezone.timedelta(minutes=10),  # Примерное время истечения
#             amount=product.price,
#             currency="RUB",
#         )
#         return payment_session
#     else:
#         raise Exception("Failed to create payment session")

def check_payment_status(session_id):
    """
    Проверяет статус платежа по session_id.
    """
    url = f"https://{PAYLER_HOST}/gapi/GetStatus"
    data = {
        "key": PAYLER_API_KEY,
        "session_id": session_id
    }
    response = requests.post(url, data=data)
    response_data = response.json()
    
    # Логирование ответа
    logger.info(f"Ответ от Payler для проверки статуса: {response_data}")

    if response_data.get("status") == "Completed":
        payment_session = PaymentSession.objects.get(session_id=session_id)
        payment_session.status = "completed"
        payment_session.save()
        return "completed"
    elif response_data.get("status") == "Declined":
        payment_session = PaymentSession.objects.get(session_id=session_id)
        payment_session.status = "failed"
        payment_session.save()
        return "failed"
    else:
        return "pending"




def create_payment_session(account, products, total_amount):
    """
    Создаёт платёжную сессию с Payler для указанного аккаунта и списка продуктов.
    """
    order_id = generate_order_id()  # Генерация уникального идентификатора заказа
    url = f"https://{PAYLER_HOST}/gapi/StartSession"
    
    
    # Формируем строку с названиями всех продуктов
    product_names = ', '.join(product.title for product in products)
    
    # Отправляем запрос в Payler
    data = {
        "key": PAYLER_API_KEY,
        "type": "OneStep",
        "order_id": order_id,
        "amount": int(total_amount * 100),  # Payler требует сумму в минимальных единицах (копейках)
        "currency": "KGS",
        "product": product_names,  # Передаем все продукты в виде строки
        "return_url_success": "https://koreacenter.kg/success",
        "return_url_decline": "https://koreacenter.kg/decline",
    }

    response = requests.post(url, data=data)
    response_data = response.json()
    
    # Логирование ответа от Payler
    logger.info(f"Ответ от Payler для создания сессии: {response_data}")

    if response_data.get("session_id"):
        # Создаем сессию платежа для всех выбранных продуктов
        payment_session = PaymentSession.objects.create(
            account=account,
            session_id=response_data["session_id"],
            order_id=order_id,
            status="pending",
            valid_through=timezone.now() + timezone.timedelta(minutes=10),  # Примерное время истечения
            amount=total_amount,
            currency="KGS",
        )

        # Создаем связь с продуктами (если нужно)
        payment_session.products.set(products)  # Если вы используете Many-to-Many связь
        payment_session.save()

        return payment_session
    else:
        raise Exception("Failed to create payment session")