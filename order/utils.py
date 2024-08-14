from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation_email(user_email, order_id):
    subject = 'Order Confirmation'
    message = f'Your order #{order_id} has been successfully placed.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
