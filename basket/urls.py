from django.urls import path
from .views import BasketView,DeleteBasketItemView

urlpatterns = [
    path('basket/', BasketView.as_view(), name='basket'),  # URL to view the basket
    path('basket/item/delete/', DeleteBasketItemView.as_view(), name='delete_basket_item'),

]