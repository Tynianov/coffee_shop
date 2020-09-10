from django.db import models
from django.utils.translation import ugettext_lazy as _

from user.models import User
from voucher.models import Voucher


class ScanLogEntryQuerySet(models.QuerySet):
    def voucher_logs(self):
        return self.filter(type=ScanLogEntry.VOUCHER)

    def user_logs(self):
        return self.filter(type=ScanLogEntry.USER)

    def get_for_initiator(self, initiator):
        return self.filter(initiator=initiator)


class ScanLogEntry(models.Model):
    VOUCHER, USER = 'voucher', 'user'
    TYPE_CHOICES = (
        (VOUCHER, _("voucher")),
        (USER, _("User"))
    )

    created = models.DateTimeField(
        _("Creation date"),
        auto_now_add=True
    )
    type = models.CharField(
        choices=TYPE_CHOICES,
        max_length=7
    )
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='scan_logs'
    )
    status = models.BooleanField(
        _("Successfully scanned?"),
        default=False
    )
    error_message = models.CharField(
        _("Error message"),
        max_length=512,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    voucher = models.ForeignKey(
        Voucher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    objects = ScanLogEntryQuerySet.as_manager()

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Scan log")
        verbose_name_plural = _("Scan logs")

    def __str__(self):
        return f'Log #{self.pk}'
