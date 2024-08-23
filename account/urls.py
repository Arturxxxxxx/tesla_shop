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
from .views import RegisterView, VerifyCodeView, CustomTokenObtainPairView, CustomTokenRefreshView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserDetailView.as_view(), name='user-detali'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
