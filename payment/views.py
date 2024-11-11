import requests
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from cards.models import Product
from account.models import CustomUser
from .utils import create_payment_session, check_payment_status, handle_successful_payment
from .models import PaymentSession, Payment
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from decouple import config
import logging

PAYLER_HOST = config('PAYLER_HOST')
PAYLER_KEY = config('PAYLER_KEY')
BANK_AUTH_HASH = config('BANK_AUTH_HASH')

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
            print(e)
            # return JsonResponse({"error": str(e)}, status=400)


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

class StartPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        phone = request.data.get("phone")
        amount = request.data.get("amount")  # Сумма в тыйынах
        comment = f"Payment for product {product_id} by user {user.id}"
        
        # Поиск продукта и создание уникального идентификатора quid
        product = Product.objects.get(id=product_id)
        quid = f"CBK{user.id}{product_id}{Payment.objects.count()}"
        
        # Шаг 1: Проверка реквизитов
        check_response = requests.get(
            f"https://ibank2.cbk.kg/otp/check?phone={phone}",
            headers={
                "authenticate": BANK_AUTH_HASH,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        if check_response.json().get("code") != 0:
            return Response({"error": "Пользователь не найден в системе банка."}, status=400)
        
        # Шаг 2: Создание платежа
        create_response = requests.get(
            f"https://ibank2.cbk.kg/otp/create?phone={phone}&amount={amount}&quid={quid}&comment={comment}",
            headers={
                "authenticate": BANK_AUTH_HASH,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        create_data = create_response.json()
        
        if create_data.get("code") == 110:  # Успешно
            Payment.objects.create(
                user=user,
                product=product,
                amount=amount,
                quid=quid,
                txn_id=create_data["txnId"],
                status="Создан"
            )
            return Response({"message": "Платеж успешно создан", "quid": quid})
        return Response({"error": create_data.get("comment")}, status=400)

class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        quid = request.data.get("quid")
        otp = request.data.get("otp")
        
        # Подтверждение платежа
        confirm_response = requests.get(
            f"https://ibank2.cbk.kg/otp/confirm?quid={quid}&otp={otp}",
            headers={
                "authenticate": BANK_AUTH_HASH,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        confirm_data = confirm_response.json()
        
        # Обновление статуса платежа на основании ответа
        payment = Payment.objects.get(quid=quid)
        payment.status = "Подтвержден" if confirm_data.get("code") == 220 else "Неудача"
        payment.save()
        
        return Response({"message": confirm_data.get("comment")})
    

class CheckPaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quid = request.query_params.get("quid")
        
        # Проверка, что `quid` передан
        if not quid:
            return Response({"error": "Необходимо передать параметр 'quid'."}, status=400)

        # Проверка статуса платежа через банк
        response = requests.get(
            f"https://ibank2.cbk.kg/otp/status?quid={quid}",
            headers={
                "authenticate": BANK_AUTH_HASH,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        
        status_data = response.json()
        
        # Обновление статуса платежа в базе данных, если найдено
        try:
            payment = Payment.objects.get(quid=quid)
            if status_data["code"] == 330:
                payment.status = "Успешен"
            elif status_data["code"] == 332:
                payment.status = "Неудача"
            elif status_data["code"] == 331:
                payment.status = "В процессе"
            payment.save()
        except Payment.DoesNotExist:
            return Response({"error": "Платеж с таким quid не найден."}, status=404)
        
        # Возвращаем ответ со статусом
        return Response({
            "message": status_data.get("comment"),
            "status": payment.status,
            "txn_id": status_data.get("txnId")
        })