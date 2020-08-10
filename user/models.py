from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from utils.funcs import get_backend_url


class User(AbstractUser):
    instagram_username = models.CharField(
        _("Instagram Profile"),
        max_length=30,
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        _("Phone number"),
        max_length=16,
        null=True,
        blank=True
    )
    email = models.EmailField(
        _("Email address"),
        max_length=255,
        unique=True
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'last_name', 'first_name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def create_qr_code(self):
        from qr_code.models import UserQRCode

        code = UserQRCode.objects.create(user=self)
        path = reverse('scan-user-code', args=(self.pk, ))
        url = f"{get_backend_url()}{path}"
        code.create_code(url, filename=self.email)
        return code


@receiver(post_save, sender=User)
def create_user_qr_code(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'qr_code'):
            instance.create_qr_code()
