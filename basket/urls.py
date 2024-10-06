from django.urls import path
from .views import BasketView,DeleteBasketItemView

urlpatterns = [
    path('carts/', BasketView.as_view(), name='basket'),  # URL to view the basket
    path('item/<int:product_id>/', DeleteBasketItemView.as_view(), name='delete_basket_item'),

]