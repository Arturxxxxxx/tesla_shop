from django.urls import path
from .views import StartPaymentSessionView, PaymentStatusView, FindSessionView, StartPaymentView, ConfirmPaymentView, CheckPaymentStatusView

urlpatterns = [
    path("start-payment/", StartPaymentSessionView.as_view(), name="start_payment"),
    path("payment-status/<str:session_id>/", PaymentStatusView.as_view(), name="payment_status"),
    path('find-session/<str:order_id>/', FindSessionView.as_view(), name='find_session'),
    path('mbank-payment/', StartPaymentView.as_view(), name='mbank-payment'),
    path('confirm-confirm/', ConfirmPaymentView.as_view(), name='confirm-confirm'),
    path('check-payment', CheckPaymentStatusView.as_view(), name='check-payment')

]

