from django.contrib import admin

from .models import PasswordResetSMSCode


@admin.register(PasswordResetSMSCode)
class PasswordResetSMSCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'phone_number']

