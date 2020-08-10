from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import ugettext_lazy as _

from utils.funcs import get_absolute_url
from voucher.serializers import UserDetailsVoucherSerializer
from voucher.models import Voucher, VoucherConfig
from .models import User


class CustomRegistrationSerializer(RegisterSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField()
    instagram_username = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)

    def get_cleaned_data(self):
        super(CustomRegistrationSerializer, self).get_cleaned_data()
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'instagram_username': self.validated_data.get('instagram_username', ''),
            'birth_date': self.validated_data.get('birth_date', '')
        }

    def save(self, request):
        user = super(CustomRegistrationSerializer, self).save(request)
        cleaned_data = self.get_cleaned_data()
        User.objects.filter(pk=user.pk).update(**{
            'phone_number': cleaned_data.get('phone_number', None),
            'instagram_username': cleaned_data.get('instagram_username', None),
            'birth_date': cleaned_data.get('birth_date', None)
        })
        return user


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
            "is_staff",
            "birth_date"
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
