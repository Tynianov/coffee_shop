from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class PasswordResetSMSCode(models.Model):
    code = models.CharField(
        _("Password reset SMS code"),
        max_length=6
    )
    phone_number = PhoneNumberField(
        _("Phone number")
    )
    created = models.DateTimeField(
        _("Creation date"),
        auto_now_add=True
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Password reset SMS code")
        verbose_name_plural = _("Password reset SMS codes")

