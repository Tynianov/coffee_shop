from datetime import timedelta

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from logs.models import ScanLogEntry
from utils.funcs import get_absolute_url
from menu.serializers import ProductSerializer
from user.utils import send_push_notification
from user.constants import *

from .models import Voucher, VoucherConfig


class VoucherConfigSerializer(serializers.ModelSerializer):
    free_item = ProductSerializer()

    class Meta:
        model = VoucherConfig
        fields = "__all__"


class VoucherSerializer(serializers.ModelSerializer):
    voucher_config = VoucherConfigSerializer()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    expiration_date = serializers.SerializerMethodField()
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = Voucher
        fields = [
            "is_scanned",
            "is_active",
            "created",
            "expiration_date",
            "voucher_config",
            "user",
            "qr_code",
        ]

    def get_expiration_date(self, obj):
        if obj.voucher_config.duration:
            return obj.created + timedelta(days=obj.voucher_config.duration)
        return None

    def get_qr_code(self, obj):
        if hasattr(obj, "qr_code"):
            return get_absolute_url(obj.qr_code.qr_code.url)
        return None


class UserDetailsVoucherSerializer(serializers.ModelSerializer):
    expiration_date = serializers.SerializerMethodField()
    qr_code = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    free_item = serializers.SerializerMethodField()

    class Meta:
        model = Voucher
        fields = [
            "qr_code",
            "expiration_date",
            "discount",
            "amount",
            "id",
            "title",
            "description",
            "free_item"
        ]

    def get_expiration_date(self, obj):
        if obj.voucher_config.duration:
            expiration_date = obj.created + timedelta(days=obj.voucher_config.duration)
            return expiration_date.strftime("%d/%m/%Y %H:%M")
        return None

    def get_qr_code(self, obj):
        if hasattr(obj, "qr_code"):
            return get_absolute_url(obj.qr_code.qr_code.url)
        return None

    def get_discount(self, obj):
        return obj.voucher_config.discount

    def get_amount(self, obj):
        if (
            obj.voucher_config.amount
            and obj.voucher_config.discount != VoucherConfig.FREE_ITEM
        ):
            if obj.voucher_config.amount - int(obj.voucher_config.amount):
                return "%.2f" % obj.voucher_config.amount
            return "{:g}".format(float(obj.voucher_config.amount))
        return None

    def get_title(self, obj):
        return obj.voucher_config.name

    def get_description(self, obj):
        return obj.voucher_config.description

    def get_free_item(self, obj):
        if obj.voucher_config.discount == VoucherConfig.FREE_ITEM and obj.voucher_config.free_item:
            return ProductSerializer(obj.voucher_config.free_item).data
        return None


class ScanVoucherSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        id = attrs.get("id")
        voucher = Voucher.objects.filter(id=id).first()
        log_data = {
            "type": ScanLogEntry.VOUCHER,
            "initiator": self.context.get("initiator"),
        }
        today = timezone.localtime()
        error_message = None

        if not voucher:
            error_message = _("Invalid voucher QR code")
            log_data.update({"error_message": error_message, "status": False})
            ScanLogEntry.objects.create(**log_data)
            raise serializers.ValidationError({"message": error_message})

        log_data.update({"voucher": voucher})

        if voucher.is_scanned:
            error_message = _("QR code has already been scanned")

        if voucher.expiration_date and voucher.expiration_date < today:
            error_message = _(
                f"Voucher expired {voucher.expiration_date.strftime('%m/%d/%Y')}"
            )

        if not voucher.is_active:
            error_message = _("Voucher is inactive")

        if error_message:
            log_data.update({"error_message": error_message, "status": False})
            ScanLogEntry.objects.create(**log_data)

            if voucher and voucher.user:
                push_notification_data = {
                    "code": VOUCHER_DID_NOT_SCANNED,
                }
                send_push_notification(
                    voucher.user, error_message, push_notification_data
                )

            raise serializers.ValidationError({"message": error_message})

        log_data.update({"status": True})
        ScanLogEntry.objects.create(**log_data)
        voucher.is_scanned = True
        voucher.save()
        self.voucher = voucher
        push_notification_data = {"code": VOUCHER_SCANNED, "voucher_id": voucher.id}
        send_push_notification(voucher.user, "Voucher scanned", push_notification_data)

        return attrs
