from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.constants import ROLE_CUSTOMER
from users.models import User


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            RefreshToken(attrs["refresh"]).blacklist()
        except TokenError:
            raise serializers.ValidationError(
                {"refresh": "Invalid or expired refresh token."}
            )
        return attrs

    def create(self, validated_data):
        return validated_data

class CreateCustomerSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    modified_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    role = serializers.HiddenField(
        default=ROLE_CUSTOMER,
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'customer_code', 'phone', 'first_name', 'last_name', 'address', 'opening_balance', 'created_at', 'modified_at' ,'created_by', 'modified_by', 'role']
        read_only_fields = ['id', 'created_at', 'modified_at']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': True},
            'customer_code': {'required': True},
            'address': {'required': True},
        }


class UpdateCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email','customer_code','phone', 'first_name', 'last_name',
            'address', 'opening_balance',
            'modified_by',
        ]


class ReadCustomerSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True,allow_null=True)
    modified_by = serializers.CharField(source='modified_by.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'customer_code', 'phone', 'first_name', 'last_name',
            'address', 'opening_balance', 'created_at', 'modified_at', 'created_by', 'modified_by'
        ]
        read_only_fields = fields

