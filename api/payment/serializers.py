from rest_framework import serializers

from api.payment.models import Payment


class PaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Please enter an amount greater than 0.'
            )
        return value
