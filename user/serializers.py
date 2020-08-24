import random
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from utils.funcs import get_absolute_url
from voucher.serializers import UserDetailsVoucherSerializer
from voucher.models import Voucher, VoucherConfig
from sms.models import PasswordResetSMSCode
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User


class CustomRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False)
    phone_number = PhoneNumberField()
    instagram_username = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)

    def get_cleaned_data(self):
        super(CustomRegistrationSerializer, self).get_cleaned_data()
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
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

    def validate_phone_number(self, val):
        if User.objects.filter(phone_number=val).exists():
            raise serializers.ValidationError({"error": _("User with this phone number already registered")})

        return val


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


class PasswordResetBySMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')

        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            raise serializers.ValidationError({
                'error': _("User with entered phone number not found")
            })

        PasswordResetSMSCode.objects.create(**{
            "phone_number": phone_number,
            "code": self.generate_sms_code()
        })
        #TODO send code by SMS
        return attrs

    def generate_sms_code(self):
        code = ''
        while True:
            rnd_numbers = ["%02d" % random.randint(0, 99) for i in range(3)]
            code = ''.join(rnd_numbers)
            if not PasswordResetSMSCode.objects.filter(code=code).exists():
                break
        return code


class ValidatePasswordResetPasswordCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
    phone_number = serializers.CharField()

    def validate(self, attrs):
        sms_code = attrs.get('code')
        phone_number = attrs.get('phone_number')

        code = PasswordResetSMSCode.objects.filter(code=sms_code).first()

        if not code:
            raise serializers.ValidationError({'error': _("Invalid code")})

        if phone_number != code.phone_number:
            raise serializers.ValidationError({
                "error": _("Error occurred while phone number validation")
            })

        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            raise serializers.ValidationError({
                "error": _("User with entered phone number not found")
            })
        self.user = user

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        repeat_password = attrs.get('repeat_password')
        if new_password != repeat_password:
            raise serializers.ValidationError({'error': _('Passwords must match')})
        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value


class CustomLoginSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'})
    phone_number = serializers.CharField()

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)
    
    def _validate_phone_number(self, phone_number, password):
        user = None

        if phone_number and password:
            user = self.authenticate(phone_number=phone_number, password=password)
        else:
            raise serializers.ValidationError({"error": _("Must include phone number and password")})

        return user

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        
        user = self._validate_phone_number(phone_number, password)
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError({"error": msg})
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError({"error": msg})

        attrs['user'] = user
        return attrs
