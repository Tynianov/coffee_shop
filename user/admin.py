from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm

from qr_code.models import UserQRCode
from .models import User


class UserQRCodeInline(admin.TabularInline):
    model = UserQRCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'first_name', 'last_name']
    inlines = [UserQRCodeInline]
    form = UserChangeForm
