from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.product.models import Product, ProductVariant

from .serializers import ProductSerializers, ProductVariantSerializers


class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializers(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductVariantList(APIView):
    def get(self, request):
        variants = ProductVariant.objects.all()
        serializer = ProductVariantSerializers(variants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductVariantSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductVariantDetail(APIView):
    def get_object(self, pk):
        try:
            return ProductVariant.objects.get(pk=pk)
        except ProductVariant.DoesNotExist as exc:
            raise Http404 from exc

    def get(self, request, pk):
        variant = self.get_object(pk)
        serializer = ProductVariantSerializers(variant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        variant = self.get_object(pk)
        serializer = ProductVariantSerializers(variant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        variant = self.get_object(pk)
        variant.status = ProductVariant.STATUS_INACTIVE
        variant.save(update_fields=["status", "updated_at"])
        serializer = ProductVariantSerializers(variant)
        return Response(serializer.data, status=status.HTTP_200_OK)