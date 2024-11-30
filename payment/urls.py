from django.urls import path
from .views import StartPaymentSessionView, PaymentStatusView, FindSessionView, LastOrderDetailView, OrderCreateView, AdminOrderListView

urlpatterns = [
    path("start-payments/", StartPaymentSessionView.as_view(), name="start_payment"),
    path("payments-status/<str:session_id>/<str:order_id>/", PaymentStatusView.as_view(), name="payment_status"),
    path('find-session/<str:order_id>/', FindSessionView.as_view(), name='find_session'),
    path('payments-history/', LastOrderDetailView.as_view(), name='payments-history'),
    path('orders/create/', OrderCreateView.as_view(), name='create-order'),
    path('payments-admin/', AdminOrderListView.as_view(), name='payments-admin')
]

