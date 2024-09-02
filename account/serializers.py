from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .tasks import send_activation_code
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class  Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'date_joined', 'is_active']


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'password', 'password_confirm']  # Изменено на 'phone_number'

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        # Создаем пользователя с полями phone_number, first_name и last_name
        user = User(
            phone_number=validated_data['phone_number'],
            first_name=first_name,
            last_name=last_name
        )  # Изменено на 'phone_number'
        user.set_password(password)
        user.save()

        # Создаем запись PhoneNumberVerification с активационным кодом
        verification, created = CustomUser.objects.get_or_create(
            phone_number=user.phone_number
        )
        if not created:
            verification.create_verification_code()  # Это вызовет метод create_verification_code() который создаст новый verification_code

        # Запускаем задачу Celery
        send_activation_code.delay(verification.verification_code, user.phone_number)  # Изменено на 'phone_number'
        # print(verification.verification_code)
        return user

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data
    
class CustomTokenObtainPaisSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Получаем стандартный токен
        token = super().get_token(user)

        # Добавляем кастомные поля в токен
        token['phone_number'] = user.phone_number
        # Можно добавить другие поля, например:
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Добавляем дополнительные данные в ответ
        data['user_id'] = self.user.id

        return data
    

class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=50)

    def validate_phone_number(self, value):
        if not CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона не найден.")
        return value


    
class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=50)
    verification_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Пароли не совпадают.")
        
        try:
            user = CustomUser.objects.get(phone_number=data['phone_number'], verification_code=data['verification_code'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Неверный номер телефона или код подтверждения.")
        
        if not user.is_code_valid():
            raise serializers.ValidationError("Код подтверждения истек.")
        
        return data