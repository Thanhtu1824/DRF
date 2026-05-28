from rest_framework import serializers

from api.voucher.models import Voucher


class VoucherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'used_count']

    def validate(self, attrs):
        start_at = attrs.get('start_at', getattr(self.instance, 'start_at', None))
        end_at = attrs.get('end_at', getattr(self.instance, 'end_at', None))
        discount_type = attrs.get(
            'discount_type',
            getattr(self.instance, 'discount_type', None),
        )
        discount_value = attrs.get(
            'discount_value',
            getattr(self.instance, 'discount_value', None),
        )
        max_discount_value = attrs.get(
            'max_discount_value',
            getattr(self.instance, 'max_discount_value', None),
        )

        if start_at and end_at and end_at <= start_at:
            raise serializers.ValidationError(
                {'end_at': 'end_at must be greater than start_at.'}
            )

        if discount_value is not None and discount_value <= 0:
            raise serializers.ValidationError(
                {'discount_value': 'discount_value must be greater than 0.'}
            )

        if discount_type == Voucher.TYPE_PERCENT and discount_value and discount_value > 100:
            raise serializers.ValidationError(
                {'discount_value': 'Percent discount must be less than or equal to 100.'}
            )

        if max_discount_value is not None and max_discount_value <= 0:
            raise serializers.ValidationError(
                {'max_discount_value': 'max_discount_value must be greater than 0.'}
            )

        return attrs
