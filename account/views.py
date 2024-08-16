from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema


from .serializers import RegisterSerializer, CustomTokenRefreshSerializer, CustomTokenObtainPaisSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .utils import send_sms  # Убедитесь, что эта функция импортирована правильно

User = get_user_model()

class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # Отправка SMS с активационным кодом
            # send_sms(user.phone_number, f"Your code is: {user.verification_code}")
            return Response({'message': 'Successfully registered! Check your phone for activation.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')

        if not phone or not verification_code:
            return Response({"error": "Phone number and activation code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone, verification_code=verification_code)
        except User.DoesNotExist:
            return Response({"error": "Invalid phone number or activation code."}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({"error": "This account is already activated."}, status=status.HTTP_400_BAD_REQUEST)

        user.verification_code = ''  # Очищаем активационный код после успешного подтверждения
        user.is_active = True       # Активируем пользователя
        user.save()

        return Response({"message": "Account successfully activated!"}, status=status.HTTP_200_OK)

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPaisSerializer
