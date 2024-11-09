import requests
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from cards.models import Product
from account.models import CustomUser
from .utils import create_payment_session, check_payment_status, handle_successful_payment
from .models import PaymentSession
from decouple import config
import logging

PAYLER_HOST = config('PAYLER_HOST')
PAYLER_KEY = config('PAYLER_KEY')

logger = logging.getLogger(__name__)

class StartPaymentSessionView(APIView):
    def post(self, request):
        product_ids = request.data.get("product_ids", [])
        account = get_object_or_404(CustomUser, id=request.user.id)

        # Проверка наличия активных продуктов
        products = Product.objects.filter(id__in=product_ids)
        if not products:
            return JsonResponse({"error": "No active products found"}, status=400)

        total_amount = sum(product.price for product in products)

        try:
            payment_session = create_payment_session(account, products, total_amount)

            pay_url = f"https://{PAYLER_HOST}/gapi/Pay?session_id={payment_session.session_id}"
            return JsonResponse({"pay_url": pay_url})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class PaymentStatusView(APIView):
    def get(self, request, session_id):
        status = check_payment_status(session_id)
        return JsonResponse({"status": status})


class FindSessionView(APIView):
    def get(self, request, order_id):
        url = f"https://{PAYLER_HOST}/gapi/FindSession"
        params = {"key": PAYLER_KEY, "order_id": order_id}

        logger.info(f"Отправка запроса для поиска сессии с order_id={order_id}")

        try:
            response = requests.get(url, params=params)
            response_data = response.json()
            
            logger.info(f"Получен ответ: {response_data}")

            if response.status_code == 200:
                return JsonResponse(response_data, status=200)
            else:
                logger.error(f"Ошибка при поиске сессии: {response_data.get('message', 'Неизвестная ошибка')}")
                return JsonResponse({"error": response_data.get("message", "Ошибка при поиске сессии")}, status=response.status_code)

        except requests.RequestException as e:
            logger.error(f"Ошибка запроса к Payler API: {str(e)}")
            return JsonResponse({"error": "Ошибка запроса к Payler API"}, status=500)

# import requests
# from django.utils import timezone
# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
# from rest_framework.views import APIView
# from cards.models import Product
# from account.models import CustomUser
# from .utils import create_payment_session, check_payment_status, handle_successful_payment
# from .models import PaymentSession
# from decouple import config
# import logging
# import uuid  # импортируем модуль для генерации UUID

# PAYLER_HOST = config('PAYLER_HOST')
# PAYLER_KEY = config('PAYLER_KEY')

# logger = logging.getLogger(__name__)

# class StartPaymentSessionView(APIView):
#     def post(self, request):
#         product_ids = request.data.get("product_ids", [])
#         account = get_object_or_404(CustomUser, id=request.user.id)

#         # Проверка наличия активных продуктов
#         products = Product.objects.filter(id__in=product_ids)
#         if not products:
#             return JsonResponse({"error": "No active products found"}, status=400)

#         total_amount = sum(product.price for product in products)

#         # # Генерируем уникальный order_id
#         # order_id = uuid.uuid4()

#         try:
#             # Создаем сессию платежа и сохраняем в модели PaymentSession
#             payment_session = PaymentSession.objects.create(
#                 account=account,
#                 session_id="",  # временно пустое значение, будет установлено после создания
#                 order_id=order_id,
#                 valid_through=timezone.now() + timezone.timedelta(minutes=15),  # например, 15 минут
#                 amount=total_amount,
#                 currency="KGS",  # Укажите вашу валюту
#                 status="pending"
#             )

#             # Вызываем функцию для создания сессии и обновляем session_id в модели
#             created_session = create_payment_session(account, products, total_amount, order_id)
#             payment_session.session_id = created_session.session_id
#             payment_session.save()

#             pay_url = f"https://{PAYLER_HOST}/gapi/Pay?session_id={payment_session.session_id}"
#             return JsonResponse({"pay_url": pay_url, "order_id": str(order_id)})

#         except Exception as e:
#             logger.error(f"Ошибка при создании платежной сессии: {str(e)}")
#             return JsonResponse({"error": str(e)}, status=400)


# class PaymentStatusView(APIView):
#     def get(self, request, session_id):
#         status = check_payment_status(session_id)
#         return JsonResponse({"status": status})


# class FindSessionView(APIView):
#     def get(self, request, order_id):
#         url = f"https://{PAYLER_HOST}/gapi/FindSession"
#         params = {"key": PAYLER_KEY, "order_id": order_id}

#         logger.info(f"Отправка запроса для поиска сессии с order_id={order_id}")

#         try:
#             response = requests.get(url, params=params)
#             response_data = response.json()
            
#             logger.info(f"Получен ответ: {response_data}")

#             if response.status_code == 200:
#                 return JsonResponse(response_data, status=200)
#             else:
#                 logger.error(f"Ошибка при поиске сессии: {response_data.get('message', 'Неизвестная ошибка')}")
#                 return JsonResponse({"error": response_data.get("message", "Ошибка при поиске сессии")}, status=response.status_code)

#         except requests.RequestException as e:
#             logger.error(f"Ошибка запроса к Payler API: {str(e)}")
#             return JsonResponse({"error": "Ошибка запроса к Payler API"}, status=500)
