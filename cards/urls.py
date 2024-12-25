from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, MarkaViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'Marka', MarkaViewSet)  # Используем 'products' вместо 'product'

urlpatterns = [
    path('', include(router.urls))
]  