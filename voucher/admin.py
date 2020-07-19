from django.contrib import admin

from .models import VoucherConfig


@admin.register(VoucherConfig)
class VoucherConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'type']
