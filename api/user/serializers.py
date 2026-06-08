from rest_framework import serializers

from api.user.models import User, UserAddress


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'role',
            'avatar',
            'status',
        ]
        read_only_fields = fields


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

    def _is_admin(self):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and request.user.is_admin_role()
        )

    def validate(self, attrs):
        is_admin = self._is_admin()

        if self.instance is None:
            if not is_admin:
                attrs['role'] = User.ROLE_CUSTOMER
                attrs['status'] = User.STATUS_ACTIVE
            return attrs

        if not is_admin:
            if 'role' in attrs and attrs['role'] != self.instance.role:
                raise serializers.ValidationError(
                    {
                        'role': (
                            'You cannot change your role. '
                            'Please contact an admin if you need help.'
                        ),
                    }
                )
            if 'status' in attrs and attrs['status'] != self.instance.status:
                raise serializers.ValidationError(
                    {
                        'status': (
                            'You cannot change account status. '
                            'Please contact an admin if you need help.'
                        ),
                    }
                )
            attrs.pop('role', None)
            attrs.pop('status', None)
        elif 'status' in attrs:
            request = self.context.get('request')
            if (
                attrs['status'] == User.STATUS_INACTIVE
                and request
                and request.user.pk == self.instance.pk
            ):
                raise serializers.ValidationError(
                    {
                        'status': (
                            'You cannot deactivate your own account.'
                        ),
                    }
                )

        return attrs

    def validate_role(self, value):
        if self._is_admin():
            return value
        if value != User.ROLE_CUSTOMER:
            raise serializers.ValidationError(
                'Only an admin can assign admin, staff, or seller roles.'
            )
        return value

    def validate_status(self, value):
        if value not in (User.STATUS_ACTIVE, User.STATUS_INACTIVE):
            raise serializers.ValidationError(
                'Please choose active or inactive.'
            )
        if self._is_admin():
            return value
        if value != User.STATUS_ACTIVE:
            raise serializers.ValidationError(
                'Only an admin can set account status.'
            )
        return value

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
