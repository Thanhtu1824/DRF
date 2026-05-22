from rest_framework import status
from rest_framework.views import APIView, Http404
from rest_framework.response import Response

from api.models import Brand
from .serializers import BrandSerializers


class BrandList(APIView):
    def get(sefl, request):
        brand = Brand.objects.all()
        serializers = BrandSerializers(brand, many=True)
        return Response (serializers.data, status=status.HTTP_200_OK)
    
    def post(sefl, request):
        serializers = BrandSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        
        return Response (serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

class BrandDetail(APIView):
    def get_object(sefl, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise Http404
        
    def get(sefl, request, pk):

        brand = sefl.get_object(pk)
        serializers = BrandSerializers(brand)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def put(sefl, request, pk):
        brand = sefl.get_object(pk)
        serializers = BrandSerializers(brand, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_202_ACCEPTED) 
        
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(sefl, request, pk):
        brand=sefl.get_object(pk)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
