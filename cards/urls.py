from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, MarkaSerializer

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'Marka', MarkaSerializer)  # Используем 'products' вместо 'product'

urlpatterns = [
    path('', include(router.urls))
]  