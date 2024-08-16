# from django.contrib.auth.models import AbstractUser, Permission, Group
# from django.db import models
# from django.utils.crypto import get_random_string
# from django.contrib.auth.base_user import BaseUserManager

# class UserManager(BaseUserManager):
#     def _create_user(self, phone, password=None, **extra):
#         if not phone:
#             raise ValueError('The Phone number must be set')
#         phone = self.normalize_phone(phone)
#         user = self.model(phone=phone, **extra)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, phone, password=None, **extra):
#         extra.setdefault('is_active', False)
#         return self._create_user(phone, password, **extra)

#     def create_superuser(self, phone, password=None, **extra):
#         extra.setdefault('is_active', True)
#         extra.setdefault('is_staff', True)
#         extra.setdefault('is_superuser', True)
#         return self._create_user(phone, password, **extra)

#     def normalize_phone(self, phone):
#         return phone.strip()

# class User(AbstractUser):
#     username = None
#     email = None
#     phone = models.CharField(max_length=19, unique=True)
#     is_active = models.BooleanField(default=False)
#     activation_code = models.CharField(max_length=4, blank=True)

#     USERNAME_FIELD = 'phone'
#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     def create_activation_code(self):
#         code = get_random_string(length=4, allowed_chars='0123456789')
#         self.activation_code = code
# from typing import Any
# from django.db import models
# from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin, Permission, Group
# from django.utils.crypto import get_random_string

# class UserManager(BaseUserManager):
#     def _create_user(self, phone, password=None, **extra_fields):
#         if not phone:
#             raise ValueError('Phone - поле обязательное')
#         user = self.model(phone=phone, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, phone, password=None, **extra_fields):
#         extra_fields.setdefault('is_active', False)
#         return self._create_user(phone, password, **extra_fields)

#     def create_superuser(self, phone, password=None, **extra_fields):
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(phone, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     phone = models.CharField(max_length=19, unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     activation_code = models.CharField(max_length=15, blank=True)

#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_groups',
#         blank=True,
#         help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
#         related_query_name='custom_user',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_permissions',
#         blank=True,
#         help_text=('Specific permissions for this user.'),
#         related_query_name='custom_user',
#     )

#     USERNAME_FIELD = 'phone'
#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     def create_activation_code(self):
#         self.activation_code = get_random_string(length=10, allowed_chars='0123456789')
# models.py
# from typing import Any
# from django.db import models
# from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin, Permission, Group
# from django.utils.crypto import get_random_string

# class UserManager(BaseUserManager):
#     def _create_user(self, phone, password=None, **extra_fields):
#         if not phone:
#             raise ValueError('Phone - поле обязательное')
#         phone = phone.strip()
#         user = self.model(phone=phone, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, phone, password=None, **extra_fields):
#         extra_fields.setdefault('is_active', False)
#         return self._create_user(phone, password, **extra_fields)

#     def create_superuser(self, phone, password=None, **extra_fields):
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(phone, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     phone = models.CharField(max_length=19, unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     activation_code = models.CharField(max_length=15, blank=True)

#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_groups',
#         blank=True,
#         help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
#         related_query_name='custom_user',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_permissions',
#         blank=True,
#         help_text=('Specific permissions for this user.'),
#         related_query_name='custom_user',
#     )

#     USERNAME_FIELD = 'phone'
#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     def create_activation_code(self):
#         self.activation_code = get_random_string(length=10, allowed_chars='0123456789')
#         self.save()




# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.utils import timezone

# class CustomUserManager(BaseUserManager):
#     def create_user(self, phone_number, password=None):
#         if not phone_number:
#             raise ValueError('The Phone Number field must be set')

#         user = self.model(phone_number=phone_number)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, phone_number, password=None):
#         user = self.create_user(phone_number, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

# class CustomUser(AbstractBaseUser):
#     phone_number = models.CharField(max_length=50, unique=True)

#     # required
#     date_joined = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=False)

#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.phone_number


# class PhoneNumberVerification(models.Model):
#     phone_number = models.CharField(max_length=15)
#     verification_code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.phone_number} - {self.verification_code}"
    

# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.crypto import get_random_string

class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, password, **extra):
        if not phone_number:
            raise ValueError('Phone - поле обязательное')
        user = self.model(phone_number=phone_number, **extra)
        user.set_password(password)
        user.save()
        return user


    def create_user(self, phone_number, password, **extra):
        user = self._create_user(phone_number, password, **extra)
        user.create_verification_code()
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra):
        user = self.create_user(phone_number, password, **extra)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  # Ensure the superuser is active
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, verbose_name='имя', blank=False, default='')
    last_name = models.CharField(max_length=30, verbose_name='фамилия', blank=False, default='')
    phone_number = models.CharField(max_length=50, unique=True)
    verification_code = models.CharField(max_length=6)  # Добавлено поле
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 
    expires_at = models.DateTimeField(null=True, blank=True)  # Поле для хранения времени истечения срока действия
     # Required for admin access

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def create_verification_code(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = get_random_string(length=6, allowed_chars='0123456789')
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=10)  # Установить время истечения срока действия
        super().save(*args, **kwargs)

    def is_code_valid(self):
        return timezone.now() < self.expires_at

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"{self.phone_number} - {self.verification_code}"




# class PhoneNumberVerification(models.Model):
#     phone_number = models.CharField(max_length=15, unique=True)
#     verification_code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
    # expires_at = models.DateTimeField(null=True, blank=True)  # Поле для хранения времени истечения срока действия

#     def is_expired(self):
#         return timezone.now() > self.expires_at
    
#     def save(self, *args, **kwargs):
#         if not self.verification_code:
#             self.verification_code = get_random_string(length=6, allowed_chars='0123456789')
#         if not self.expires_at:
#             self.expires_at = timezone.now() + timezone.timedelta(minutes=10)  # Установить время истечения срока действия
#         super().save(*args, **kwargs)

#     def is_code_valid(self):
#         return timezone.now() < self.expires_at

#     def __str__(self):
#         return f"{self.phone_number} - {self.verification_code}"
