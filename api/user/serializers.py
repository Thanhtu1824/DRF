from rest_framework import serializers

from api.user.models import User, UserAddress


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
            'role',
            'avatar',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'id',
            'user',
            'recipient_name',
            'phone',
            'address_line',
            'ward',
            'district',
            'province',
            'is_default',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def validate_phone(self, value):
        phone = value.strip()
        digits_only = ''.join(ch for ch in phone if ch.isdigit())

        if len(digits_only) < 10 or len(digits_only) > 11:
            raise serializers.ValidationError(
                'Phone number must contain 10-11 digits.'
            )

        return phone

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
