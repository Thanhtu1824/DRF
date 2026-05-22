from rest_framework import status
from rest_framework.views import APIView, Http404
from rest_framework.response import Response

from api.models import User
from .serializers import UserSerializers


class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializers(users, many=True)
        return Response (serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializers(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user=self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
