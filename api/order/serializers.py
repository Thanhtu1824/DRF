from rest_framework import serializers

from api.order.models import Order, OrderItem


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Please enter a quantity greater than or equal to 1.'
            )
        return value
