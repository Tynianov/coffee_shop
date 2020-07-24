from django.contrib import admin

from .models import VoucherConfig, Voucher


@admin.register(VoucherConfig)
class VoucherConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'type']


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_scanned']
