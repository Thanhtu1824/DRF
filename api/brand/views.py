from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, Http404

from api.brand.models import Brand

from .serializers import BrandSerializers


class BrandList(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializers(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BrandSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandDetail(APIView):
    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        brand = self.get_object(pk)
        serializer = BrandSerializers(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        brand = self.get_object(pk)
        serializer = BrandSerializers(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        brand = self.get_object(pk)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
