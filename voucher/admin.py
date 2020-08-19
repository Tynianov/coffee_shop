from django.contrib import admin

from .models import VoucherConfig, Voucher


@admin.register(VoucherConfig)
class VoucherConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'type']
    fields = ('name', 'description', 'type', 'discount', 'amount', 'free_item', 'purchase_count', 'duration')

    class Media:
        js = ('js/admin/voucher_discount.js', )


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_scanned']
