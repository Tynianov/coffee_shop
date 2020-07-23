from rest_framework import serializers

from .models import Voucher, VoucherConfig


class VoucherConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherConfig
        fields = "__all__"


class VoucherSerializer(serializers.ModelSerializer):
    voucher_config = VoucherConfigSerializer()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Voucher
        fields = ["is_scanned", "is_active", "created", "expiration_date", "voucher_config", "user"]
