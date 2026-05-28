from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, Http404

from api.cart.models import Cart, CartItem

from .serializers import CartItemSerializers, CartSerializers


class CartList(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        carts = Cart.objects.filter(user=request.user)
        serializer = CartSerializers(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if Cart.objects.filter(user=request.user).exists():
            return Response(
                {'detail': 'Cart already exists for this user.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CartSerializers(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            cart = serializer.save()
            return Response(
                CartSerializers(cart).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetail(APIView):
    def get_object(self, request, pk):
        try:
            return Cart.objects.get(pk=pk, user=request.user)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        cart = self.get_object(request, pk)
        serializer = CartSerializers(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        cart = self.get_object(request, pk)
        serializer = CartSerializers(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                CartSerializers(cart).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        cart = self.get_object(request, pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemList(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        items = CartItem.objects.filter(cart__user=request.user)
        serializer = CartItemSerializers(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_variant_id = request.data.get('product_variant')
        quantity = int(request.data.get('quantity', 1))

        existing = CartItem.objects.filter(
            cart=cart,
            product_variant_id=product_variant_id,
        ).first()

        if existing:
            existing.quantity += quantity
            existing.save(update_fields=['quantity', 'updated_at'])
            serializer = CartItemSerializers(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = CartItemSerializers(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            item = serializer.save()
            return Response(
                CartItemSerializers(item).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDetail(APIView):
    def get_object(self, request, pk):
        try:
            return CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        item = self.get_object(request, pk)
        serializer = CartItemSerializers(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        item = self.get_object(request, pk)
        serializer = CartItemSerializers(
            item,
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            updated = serializer.save()
            return Response(
                CartItemSerializers(updated).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        item = self.get_object(request, pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
