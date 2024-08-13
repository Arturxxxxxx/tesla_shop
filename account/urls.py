# from django.urls import path
# from .views import RegisterView, ActivationView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('activate/<str:phone>/<str:activation_code>/', ActivationView.as_view(), name='activate'),
# ]

# urls.py
# from django.urls import path
# from .views import RegisterView, ActivationView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('activate/<str:phone>/<str:activation_code>/', ActivationView.as_view(), name='activate'),
# ]



# from django.urls import path
# from .views import RegisterView, VerifyCodeView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('verify/', VerifyCodeView.as_view(), name='verify_code'),
# ]
from django.urls import path
from .views import RegisterView, VerifyCodeView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]