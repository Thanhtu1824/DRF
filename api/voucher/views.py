from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, Http404

from api.voucher.models import Voucher

from .serializers import VoucherSerializers


class VoucherList(APIView):
    def get(self, request):
        vouchers = Voucher.objects.all()
        serializer = VoucherSerializers(vouchers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VoucherSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoucherDetail(APIView):
    def get_object(self, pk):
        try:
            return Voucher.objects.get(pk=pk)
        except Voucher.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        voucher = self.get_object(pk)
        serializer = VoucherSerializers(voucher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        voucher = self.get_object(pk)
        serializer = VoucherSerializers(voucher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        voucher = self.get_object(pk)
        voucher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
