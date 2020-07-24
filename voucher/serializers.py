from datetime import timedelta
from rest_framework import serializers

from utils.funcs import get_absolute_url
from .models import Voucher, VoucherConfig


class VoucherConfigSerializer(serializers.ModelSerializer):
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
        fields = ["is_scanned", "is_active", "created", "expiration_date", "voucher_config", "user", "qr_code"]

    def get_expiration_date(self, obj):
        if obj.voucher_config.duration:
            return obj.created + timedelta(days=obj.voucher_config.duration)
        return None

    def get_qr_code(self, obj):
        if hasattr(obj, "qr_code"):
            return get_absolute_url(obj.qr_code.qr_code.url)
        return None
