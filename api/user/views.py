from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, Http404

from api.permissions import IsAdminRole, IsOwner, any_of
from api.user.models import User, UserAddress

from .serializers import UserAddressSerializer, UserSerializers

CanAccessUserProfile = any_of(
    IsAdminRole,
    IsOwner,
    message='You can only access your own account.',
)


class UserList(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAdminRole()]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializers(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializers(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated, CanAccessUserProfile]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializers(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializers(
            user,
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = self.get_object(pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializers(
            user,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = UserAddress.objects.filter(user=request.user)
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserAddressSerializer(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            address = serializer.save()
            if address.is_default:
                UserAddress.objects.filter(user=request.user).exclude(
                    pk=address.pk
                ).update(is_default=False)
            response_serializer = UserAddressSerializer(address)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressDetail(APIView):
    def get_object(self, request, pk):
        try:
            return UserAddress.objects.get(pk=pk, user=request.user)
        except UserAddress.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        address = self.get_object(request, pk)
        serializer = UserAddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        address = self.get_object(request, pk)
        serializer = UserAddressSerializer(
            address,
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            updated_address = serializer.save()
            if updated_address.is_default:
                UserAddress.objects.filter(user=request.user).exclude(
                    pk=updated_address.pk
                ).update(is_default=False)
            response_serializer = UserAddressSerializer(updated_address)
            return Response(
                response_serializer.data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object(request, pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
