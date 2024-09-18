from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ForgotPasswordSerializer, VerifyResetCodeSerializer, ResetPasswordSerializer
from .models import CustomUser
from .tasks import send_activation_code
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema


from .serializers import RegisterSerializer, CustomTokenRefreshSerializers, CustomTokenObtainPairSerializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

User = get_user_model()

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию для этого view

    def get(self, request):
        user = request.user  # Получаем текущего пользователя из request
        serializer = UserSerializer(user)  # Сериализуем данные пользователя
        return Response(serializer.data)  

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
        
        # Проверка срока действия кода верификации
        if user.is_expired():
            return Response({"error": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)


        if user.is_active:
            return Response({"error": "This account is already activated."}, status=status.HTTP_400_BAD_REQUEST)

        user.verification_code = ''  # Очищаем активационный код после успешного подтверждения
        user.expires_at = None       # Очищаем поле expires_at
        user.is_active = True       # Активируем пользователя
        user.save()

        return Response({"message": "Account successfully activated!"}, status=status.HTTP_200_OK)

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializers

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializers

class ResendVerificationCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        user.create_verification_code()
        user.save()

        
class ForgotPasswordPhoneView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Получаем пользователя
            user = CustomUser.objects.get(phone_number=phone_number)

            # Генерация нового кода верификации
            user.create_verification_code()
            user.save()

            # Отправляем код на телефон пользователя
            send_activation_code.delay(user.verification_code, user.phone_number)

            return Response({"message": "Код для восстановления пароля отправлен на ваш номер телефона."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class VerifyResetCodeView(APIView):
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        if serializer.is_valid():
            verification_code = serializer.validated_data['verification_code']
            try:
                user = CustomUser.objects.get(verification_code=verification_code)
            except CustomUser.DoesNotExist:
                return Response({"error": "Invalid reset code."}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_expired():
                return Response({"error": "Reset code has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # # Очистка кода сброса и даты истечения
            # user.verification_code = ''  
            # user.expires_at = None
            # user.save()

            return Response({"message": "Reset code is valid and has been cleared. You can now set a new password."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            new_password = serializer.validated_data['new_password']

            # Обновление пароля пользователя
            user = CustomUser.objects.get(phone_number=phone_number)
            user.set_password(new_password)
            user.verification_code = ''
            user.expires_at = None  # Очистка кода после успешного сброса пароля
            user.save()

            return Response({"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
