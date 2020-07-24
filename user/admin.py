from django.contrib import admin

from qr_code.models import UserQRCode
from .models import User


class UserQRCodeInline(admin.TabularInline):
    model = UserQRCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']
    inlines = [UserQRCodeInline]
