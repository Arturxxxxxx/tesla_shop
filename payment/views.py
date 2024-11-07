# from django.shortcuts import get_object_or_404, redirect
# from django.http import JsonResponse
# from django.views import View
# from .models import Account, Product
# from .utils import create_payment_session, check_payment_status
# from decouple import config
# import requests


# PAYLER_HOST = config('PAYLER_HOST')
# PAYLER_KEY = config('PAYLER_KEY')

# class StartPaymentSessionView(View):
#     def post(self, request, product_id):
#         account = get_object_or_404(Account, user=request.user)
#         product = get_object_or_404(Product, id=product_id)
#         try:
#             payment_session = create_payment_session(account, product)
#             pay_url = f"https://{PAYLER_HOST}/gapi/Pay?session_id={payment_session.session_id}"
#             return JsonResponse({"pay_url": pay_url})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

# class PaymentStatusView(View):
#     def get(self, request, session_id):
#         status = check_payment_status(session_id)
#         return JsonResponse({"status": status})

# class FindSessionView(View):
#     def get(self, request, order_id):
#         # URL для поиска сессии
#         url = f"https://{PAYLER_HOST}/gapi/FindSession"

#         # Параметры запроса
#         params = {
#             "key": PAYLER_KEY,  # Ваш ключ API
#             "order_id": order_id
#         }

#         # Выполнение GET-запроса к Payler
#         response = requests.get(url, params=params)
#         data = response.json()

#         # Проверка успешности запроса
#         if response.status_code == 200:
#             return JsonResponse(data, status=200)
#         else:
#             return JsonResponse(data, status=response.status_code)

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from cards.models import Product
from account.models import CustomUser
from .utils import create_payment_session, check_payment_status
from decouple import config
import logging
import requests

PAYLER_HOST = config('PAYLER_HOST')
PAYLER_KEY = config('PAYLER_KEY')

# Логирование
logger = logging.getLogger(__name__)


# class StartPaymentSessionView(View):
#     def post(self, request, product_id):
#         account = get_object_or_404(CustomUser, user=request.user)
#         product = get_object_or_404(Product, id=product_id)
#         try:
#             payment_session, acs_url, pareq = create_payment_session(account, product)
#             pay_url = f"https://{PAYLER_HOST}/gapi/Pay?session_id={payment_session.session_id}"

#             if acs_url and pareq:
#                 # Требуется 3DS, возвращаем URL и параметры для 3DS
#                 return JsonResponse({"3ds_url": acs_url, "pareq": pareq})
#             else:
#                 return JsonResponse({"pay_url": pay_url})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

class StartPaymentSessionView(View):
    def post(self, request):
        # Получаем список выбранных продуктов через POST-запрос
        product_ids = request.data.get("product_ids", [])  # В случае POST-запроса это будет список ID продуктов
        account = get_object_or_404(CustomUser, user=request.user)

        # Получаем продукты по их ID и фильтруем по активности
        products = Product.objects.filter(id__in=product_ids, is_active=True)

        if not products:
            return JsonResponse({"error": "No active products found"}, status=400)

        # Рассчитываем общую сумму для всех выбранных продуктов
        total_amount = sum(product.price for product in products)

        # Генерируем уникальный order_id для всех продуктов
        # order_id = f"order_{account.user.id}_{'_'.join(str(product.id) for product in products)}"

        # Создаём платежную сессию
        try:
            payment_session = create_payment_session(account, products, total_amount)

            # Генерация URL для перехода к оплате
            pay_url = f"https://{PAYLER_HOST}/gapi/Pay?session_id={payment_session.session_id}"

            return JsonResponse({"pay_url": pay_url})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class PaymentStatusView(View):
    def get(self, request, session_id):
        status = check_payment_status(session_id)
        return JsonResponse({"status": status})


class FindSessionView(View):
    def get(self, request, order_id):
        """
        Находит платежную сессию по order_id, отправляя запрос в Payler API.
        """
        url = f"https://{PAYLER_HOST}/gapi/FindSession"
        params = {
            "key": PAYLER_KEY,  # API-ключ
            "order_id": order_id
        }

        # Логирование перед отправкой запроса
        logger.info(f"Отправка запроса для поиска сессии с order_id={order_id}")

        try:
            response = requests.get(url, params=params)
            response_data = response.json()
            
            # Логирование ответа
            logger.info(f"Получен ответ: {response_data}")

            if response.status_code == 200:
                return JsonResponse(response_data, status=200)
            else:
                logger.error(f"Ошибка при поиске сессии: {response_data.get('message', 'Неизвестная ошибка')}")
                return JsonResponse({"error": response_data.get("message", "Ошибка при поиске сессии")}, status=response.status_code)

        except requests.RequestException as e:
            logger.error(f"Ошибка запроса к Payler API: {str(e)}")
            return JsonResponse({"error": "Ошибка запроса к Payler API"}, status=500)