from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_auth.models import TokenModel
from rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import ugettext_lazy as _

from voucher.serializers import UserDetailsVoucherSerializer
from voucher.models import Voucher, VoucherConfig
from .models import User


class CustomRegistrationSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, allow_null=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    instagram_username = serializers.CharField(required=False)


class UserSerializer(serializers.ModelSerializer):
    vouchers = UserDetailsVoucherSerializer(many=True)
    voucher_purchase_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "last_name",
            "first_name",
            "phone_number",
            "instagram_username",
            "qr_code",
            "vouchers",
            "current_purchase_count",
            "voucher_purchase_count"
        ]

    def get_voucher_purchase_count(self, obj):
        voucher_conf = VoucherConfig.objects\
            .filter(type=VoucherConfig.MIN_PURCHASE_AMOUNT)\
            .order_by('purchase_count')\
            .first()
        return voucher_conf.purchase_count


class ValidateUserQrCodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        id = attrs.get('id')
        user = User.objects.filter(id=id).first()
        if not user:
            raise serializers.ValidationError({
                'message': _("Invalid user QR code")
            })

        user.current_purchase_count += 1
        user.save()

        for voucher_config in VoucherConfig.objects.min_purchase_type():
            if voucher_config.purchase_count <= user.current_purchase_count:
                voucher_data = {
                    'user': user,
                    'voucher_config': voucher_config
                }
                if voucher_config.duration:
                    now = timezone.localtime()
                    expiration_date = now + timedelta(days=voucher_config.duration)
                    voucher_data.update({
                        'expiration_date': expiration_date
                    })
                Voucher.objects.create(**voucher_data)
                user.current_purchase_count = 0
                user.save()

        return attrs


class TokenSerializer(serializers.ModelSerializer):
    is_staff = serializers.SerializerMethodField()

    class Meta:
        model = TokenModel
        fields = ['key', 'is_staff']

    def get_is_staff(self, obj):
        return obj.user.is_staff or obj.user.is_superuser
