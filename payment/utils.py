import requests
from django.utils.crypto import get_random_string
from django.utils import timezone
from .models import PaymentSession
from decouple import config
import uuid
import logging


PAYLER_API_KEY = config('PAYLER_KEY')
PAYLER_HOST = config('PAYLER_HOST')

# Логирование
logger = logging.getLogger(__name__)

def generate_order_id():
    """Генерирует уникальный order_id для каждого платежа."""
    return str(uuid.uuid4())
    # return f"order_{get_random_string(12)}"

def check_payment_status(session_id, order_id):
    """
    Проверяет статус платежа по session_id.
    """
    url = f"https://{PAYLER_HOST}/gapi/GetStatus"
    data = {
        "key": PAYLER_API_KEY,
        "session_id": session_id,
        "order_id": order_id
    }
    response = requests.post(url, data=data)
    print(response)
    response_data = response.json()
    
    # Логирование ответа
    logger.info(f"Ответ от Payler для проверки статуса: {response_data}")

    if response_data.get("status") == "Charged":
        print(response_data.get("status"))
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
        return "pendingg"




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
        "return_url_success": "https://koreacenter.kg/profile",
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
    

# utils.py или views.py, в зависимости от места вызова
from .models import Order, OrderItem

def create_order_after_payment(client, products, total_amount, currency='сом'):
    # Генерируем уникальный order_id
    order_id = str(uuid.uuid4()).replace("-", "").upper()[:12]

    # Создаём заказ
    order = Order.objects.create(
        order_id=order_id,
        client=client,
        total_amount=total_amount,
        currency=currency,
        status='paid',  # Устанавливаем статус "оплачен"
        client_phone=client.phone_number,
    )

    # Добавляем товары в заказ
    for product_data in products:
        OrderItem.objects.create(
            order=order,
            product=product_data['product'],
            quantity=product_data['quantity'],
            price=product_data['product'].price,
        )

    return order
