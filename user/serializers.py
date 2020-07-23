from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from voucher.serializers import VoucherSerializer
from .models import User



class CustomRegistrationSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, allow_null=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    instagram_username = serializers.CharField(required=False)


class UserSerializer(serializers.ModelSerializer):
    vouchers = VoucherSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "email",
            "last_name",
            "first_name",
            "phone_number",
            "instagram_username",
            "qr_code",
            "vouchers"
        ]
