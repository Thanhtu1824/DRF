from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, Http404

from api.payment.models import Payment

from .serializers import PaymentSerializers


class PaymentList(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        payments = Payment.objects.filter(
            order__user=request.user
        ).exclude(
            payment_status=Payment.STATUS_DELETED
        )
        serializer = PaymentSerializers(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = PaymentSerializers(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data.get('order')
            if order.user_id != request.user.id:
                return Response(
                    {'detail': 'You can only create payment for your own order.'},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetail(APIView):
    def get_object(self, request, pk):
        try:
            return Payment.objects.exclude(
                payment_status=Payment.STATUS_DELETED
            ).get(
                pk=pk,
                order__user=request.user,
            )
        except Payment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        payment = self.get_object(request, pk)
        serializer = PaymentSerializers(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        payment = self.get_object(request, pk)
        serializer = PaymentSerializers(payment, data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data.get('order')
            if order and order.user_id != request.user.id:
                return Response(
                    {'detail': 'You can only update payment for your own order.'},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        payment = self.get_object(request, pk)
        payment.payment_status = Payment.STATUS_DELETED
        payment.deleted_at = timezone.now()
        payment.save(update_fields=['payment_status', 'deleted_at'])
        return Response(status=status.HTTP_204_NO_CONTENT)
