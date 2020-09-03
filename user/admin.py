from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from authtools.admin import UserAdmin, ADVANCED_PERMISSION_FIELDS, DATE_FIELDS
from qr_code.models import UserQRCode
from .models import User


class UserQRCodeInline(admin.TabularInline):
    model = UserQRCode


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["phone_number", "first_name", "last_name"]
    inlines = [UserQRCodeInline]
    form = UserChangeForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "first_name",
                    "last_name",
                    "current_purchase_count",
                    "birth_date",
                    "instagram_username",
                    "firebase_uid",
                    "password",
                )
            },
        ),
        ADVANCED_PERMISSION_FIELDS,
        DATE_FIELDS,
    )
