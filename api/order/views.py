from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, Http404

from api.order.models import Order, OrderItem

from .serializers import OrderItemSerializers, OrderSerializers


class OrderList(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializers(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = OrderSerializers(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    def get_object(self, request, pk):
        try:
            return Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        order = self.get_object(request, pk)
        serializer = OrderSerializers(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        order = self.get_object(request, pk)
        serializer = OrderSerializers(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        order = self.get_object(request, pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemList(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        order_items = OrderItem.objects.filter(order__user=request.user)
        serializer = OrderItemSerializers(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = OrderItemSerializers(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data.get('order')
            if order.user_id != request.user.id:
                return Response(
                    {'detail': 'You can only add items to your own order.'},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemDetail(APIView):
    def get_object(self, request, pk):
        try:
            return OrderItem.objects.get(pk=pk, order__user=request.user)
        except OrderItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        order_item = self.get_object(request, pk)
        serializer = OrderItemSerializers(order_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        order_item = self.get_object(request, pk)
        serializer = OrderItemSerializers(order_item, data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data.get('order')
            if order and order.user_id != request.user.id:
                return Response(
                    {'detail': 'You can only update items in your own order.'},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        order_item = self.get_object(request, pk)
        order_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
