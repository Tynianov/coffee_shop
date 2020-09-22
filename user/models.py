from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from utils.funcs import get_backend_url


class UserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password=None, is_superuser=False, is_staff=False,
                    is_active=True):
        if not phone_number:
            raise ValueError("User must have an phone number")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model()

        user.phone_number = phone_number
        user.username = phone_number
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, last_name, password=None, **extra_fields):
        return self.create_user(phone_number, first_name, last_name, password, True, True, True)


class User(AbstractUser):
    instagram_username = models.CharField(
        _("Instagram Profile"),
        max_length=30,
        null=True,
        blank=True
    )
    phone_number = PhoneNumberField(
        _("Phone number"),
        unique=True
    )
    email = models.EmailField(
        _("Email address"),
        max_length=255,
        null=True,
        blank=True
    )
    current_purchase_count = models.PositiveIntegerField(
        _("Current user purchase"),
        default=0,
        help_text=_("Count of current user purchase")
    )
    birth_date = models.DateField(
        _("Birth day"),
        null=True,
        blank=True
    )
    firebase_uid = models.CharField(
        _("Firebase user uId"),
        null=True,
        blank=True,
        max_length=1024
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def create_qr_code(self):
        from qr_code.models import UserQRCode

        code = UserQRCode.objects.create(user=self)
        path = reverse('scan-user-code', args=(self.pk,))
        url = f"{get_backend_url()}{path}"
        code.create_code(url, filename=self.email)
        return code


@receiver(post_save, sender=User)
def create_user_qr_code(sender, instance, created, **kwargs):
    if created:
        from voucher.models import VoucherConfig, Voucher

        if not hasattr(instance, 'qr_code'):
            instance.create_qr_code()

        if VoucherConfig.objects.for_registration().exists():
            voucher_conf = VoucherConfig.objects.for_registration().first()
            Voucher.objects.create(**{
                'voucher_config': voucher_conf,
                'user': instance
            })
