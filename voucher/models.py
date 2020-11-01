from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from utils.models import StatusModel, StatusQuerySet
from utils.funcs import get_backend_url
from menu.models import Product
from user.models import User


class VoucherConfigQuerySet(StatusQuerySet):
    def min_purchase_type(self):
        return self.active().filter(type=VoucherConfig.MIN_PURCHASE_AMOUNT)

    def for_registration(self):
        return self.active().filter(type=VoucherConfig.FOR_REGISTRATION)


class VoucherConfig(StatusModel):

    MIN_PURCHASE_AMOUNT, FOR_REGISTRATION, FOR_ALL_USERS = 'min_purchase_amount', 'for_registration', 'for_all_users'
    TYPE_CHOICES = (
        (MIN_PURCHASE_AMOUNT, _("Minimum purchase amount")),
        (FOR_REGISTRATION, _("For registration")),
        (FOR_ALL_USERS, _("For all users"))
    )
    FIXED, PERCENTAGE, FREE_ITEM = 'fixed', 'percentage', 'free_item'
    DISCOUNT_CHOICES = (
        (FIXED, _('Fixed discount')),
        (PERCENTAGE, _('Percentage dicount')),
        (FREE_ITEM, _('Free product'))
    )

    name = models.CharField(
        _("Voucher name"),
        max_length=256,
        help_text=_("Enter voucher name")
    )
    description = models.CharField(
        _("Voucher description"),
        max_length=512,
        blank=True,
        default='',
        help_text=_("Enter voucher description")
    )
    type = models.CharField(
        _("Voucher type"),
        choices=TYPE_CHOICES,
        max_length=32,
        help_text=_("Select voucher type (in which case user receive voucher)"),
        default=MIN_PURCHASE_AMOUNT
    )
    discount = models.CharField(
        _("Discount type"),
        choices=DISCOUNT_CHOICES,
        max_length=32,
        help_text=_("Select discount type"),
        default=FIXED
    )
    amount = models.DecimalField(
        _("Amount"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Set discount amount")
    )
    duration = models.PositiveIntegerField(
        _("Voucher duration"),
        null=True,
        blank=True,
        help_text=_("Set how much days will voucher be available after creation")
    )
    purchase_count = models.PositiveIntegerField(
        _("Purchase count"),
        null=True,
        blank=True,
        help_text=_("Set minimum purchase amount for receiving voucher")
    )
    free_item = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    objects = VoucherConfigQuerySet.as_manager()

    class Meta:
        verbose_name = _("Voucher discount")
        verbose_name_plural = _("Voucher discount")

    def __str__(self):
        return self.name

    def clean(self):
        if self.discount in [self.PERCENTAGE, self.FIXED] and not self.amount:
            raise ValidationError(_("Specify discount amount"))

        if self.discount == self.FREE_ITEM and not self.free_item:
            raise ValidationError(_("Select free item"))

        if self.type == self.MIN_PURCHASE_AMOUNT and not self.purchase_count:
            raise ValidationError(_("Specify purchase count"))


class VoucherQuerySet(StatusQuerySet):
    def not_scanned(self):
        return self.filter(is_scanned=False)

    def scanned(self):
        return self.filter(is_scanned=True)


class Voucher(StatusModel):

    voucher_config = models.ForeignKey(
        VoucherConfig,
        on_delete=models.CASCADE,
        related_name='vouchers'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vouchers'
    )
    is_scanned = models.BooleanField(
        _("Is scanned?"),
        default=False
    )
    created = models.DateTimeField(
        _("Creation date"),
        auto_now_add=True
    )
    expiration_date = models.DateTimeField(
        _("Expiration date"),
        null=True,
        blank=True
    )

    objects = VoucherQuerySet.as_manager()

    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")

    def __str__(self):
        return f"{self.voucher_config.name} - {self.user.email}"

    def create_qr_code(self):
        from qr_code.models import VoucherQRCode

        code = VoucherQRCode.objects.create(voucher=self)
        path = reverse('scan-voucher-code', args=(self.pk, ))
        url = f"{get_backend_url()}{path}"
        code.create_code(url, filename=self.pk)
        return code


@receiver(post_save, sender=Voucher)
def create_user_qr_code(sender, instance, created, **kwargs):
    if created:
        instance.create_qr_code()

