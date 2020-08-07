from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import ugettext_lazy as _

from utils.funcs import get_absolute_url
from voucher.serializers import UserDetailsVoucherSerializer
from voucher.models import Voucher, VoucherConfig
from logs.models import ScanLogEntry
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
    is_staff = serializers.SerializerMethodField()
    qr_code = serializers.SerializerMethodField()

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
            "voucher_purchase_count",
            "is_staff"
        ]

    def get_voucher_purchase_count(self, obj):
        voucher_conf = VoucherConfig.objects \
            .filter(type=VoucherConfig.MIN_PURCHASE_AMOUNT) \
            .order_by('purchase_count')
        return voucher_conf[0].purchase_count if voucher_conf.count() > 0 else 0

    def get_is_staff(self, obj):
        return obj.is_staff or obj.is_superuser

    def get_qr_code(self, obj):
        if hasattr(obj, "qr_code"):
            return get_absolute_url(obj.qr_code.qr_code.url)
        return None


class ValidateUserQrCodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        id = attrs.get('id')
        user = User.objects.filter(id=id).first()

        log_entry_data = {
            'type': ScanLogEntry.USER,
            'initiator': self.context.get('initiator')
        }

        if not user:
            error_msg = "Invalid user QR code"
            log_entry_data.update({
                'status': False,
                'error_message': error_msg
            })
            ScanLogEntry.objects.create(**log_entry_data)

            raise serializers.ValidationError({
                'message': _(error_msg)
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
        log_entry_data.update({
            'status': True,
            'user': user
        })
        ScanLogEntry.objects.create(**log_entry_data)

        return attrs


class UpdateUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "last_name",
            "first_name",
            "phone_number",
            "instagram_username"
        ]
        read_only_fields = ('email', )
