import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PaymentSerializer
from .models import Payment

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount'] * 100  # amount in cents
            currency = serializer.validated_data['currency']
            source = serializer.validated_data['source']

            try:
                charge = stripe.Charge.create(
                    amount=amount,
                    currency=currency,
                    source=source,
                    description='Payment description',
                )

                Payment.objects.create(
                    user=request.user,
                    amount=serializer.validated_data['amount'],
                    stripe_charge_id=charge.id,
                )

                return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
            except stripe.error.CardError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
