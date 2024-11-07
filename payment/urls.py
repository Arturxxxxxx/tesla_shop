from django.urls import path
from .views import StartPaymentSessionView, PaymentStatusView, FindSessionView

urlpatterns = [
    path("start-payment/", StartPaymentSessionView.as_view(), name="start_payment"),
    path("payment-status/<str:session_id>/", PaymentStatusView.as_view(), name="payment_status"),
    path('find-session/<str:order_id>/', FindSessionView.as_view(), name='find_session')
]

