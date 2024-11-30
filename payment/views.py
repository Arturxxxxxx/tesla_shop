import requests
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from cards.models import Product
from account.models import CustomUser
from .utils import create_payment_session, check_payment_status
from .models import PaymentSession, Order
from .serializers import OrderSerializer, OrderItemSerializer, OrderCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
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
            pay_url = f"https://{PAYLER_HOST}/gapi/Pay?session_id="
            return JsonResponse({"pay_url": pay_url,
                                 "payment_session": payment_session.session_id,
                                 "order_id": payment_session.order_id})
            # pay_url = f"https://{PAYLER_HOST}/gapi/Pay?session_id={payment_session.session_id}"
            # return JsonResponse({"pay_url": pay_url,
            #                      "payment_session": payment_session.session_id})

        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)})


class PaymentStatusView(APIView):
    def get(self, request, session_id, order_id):
        status = check_payment_status(session_id, order_id)
        print(status)
        return JsonResponse({"statusss": status})


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

class LastOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.requests.user
        if user.role == 'admin':
            return Order.objects.all()
        else:# Возвращаем последний заказ клиента
            return Order.objects.filter(client=self.request.user).order_by('-order_date').first()

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Автоматически добавляем текущего клиента в заказ
        serializer.save(client=self.request.user)
