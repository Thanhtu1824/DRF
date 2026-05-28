from rest_framework import serializers

from api.cart.models import Cart, CartItem


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'id',
            'cart',
            'product_variant',
            'quantity',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'cart': {'read_only': True},
        }

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Quantity must be at least 1.'
            )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            validated_data['cart'] = cart
        return super().create(validated_data)
