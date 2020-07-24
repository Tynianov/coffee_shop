from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.models import StatusModel
from user.models import User


class VoucherConfig(StatusModel):

    MIN_PURCHASE_AMOUNT, FOR_REGISTRATION, FOR_ALL_USERS = 'min_purchase_amount', 'for_registration', 'for_all_users'
    TYPE_CHOICES = (
        (MIN_PURCHASE_AMOUNT, "Минимальное кол-во покупок"),
        (FOR_REGISTRATION, "За регестрацию"),
        (FOR_ALL_USERS, "Для всех пользователей")
    )
    FIXED, PERCENTAGE, FREE_ITEM = 'fixed', 'percentage', 'free_item'
    DISCOUNT_CHOICES = (
        (FIXED, 'Фиксированная скидка'),
        (PERCENTAGE, 'Процентная скидка'),
        (FREE_ITEM, 'Бесплатный продукт')
    )

    name = models.CharField(
        "Название ваучера",
        max_length=256,
        help_text="Введите название ваучера"
    )
    description = models.CharField(
        "Описание ваучера",
        max_length=512,
        blank=True,
        default='',
        help_text="Введите опсание ваучера"
    )
    type = models.CharField(
        "Тип ваучера",
        choices=TYPE_CHOICES,
        max_length=32,
        help_text="Выберете тип ваучера (в каких случаях ользователи будут получать ваучеры)",
        default=MIN_PURCHASE_AMOUNT
    )
    discount = models.CharField(
        "Выберете тип скидки",
        choices=DISCOUNT_CHOICES,
        max_length=32,
        help_text="Выберете тип скидки",
        default=FIXED
    )
    amount = models.DecimalField(
        "Значение",
        max_digits=8,
        decimal_places=2,
        help_text="Выставите значение скидки (процент либо фиксированное значение)"
    )
    duration = models.DurationField(
        "Длительность действия",
        null=True,
        blank=True,
        help_text="Выставите, сколько ваучер будет доступен после получения"
                  " (оставьте пустым для того, что бы ваучер действовал всегда )"
    )

    class Meta:
        verbose_name = "Шаблон ваучера"
        verbose_name_plural = "Шаблоны ваучеров"


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
        "Отсканирован?",
        default=False
    )
    created = models.DateTimeField(
        "дата содания",
        auto_now_add=True
    )
    expiration_date = models.DateTimeField(
        "Дата истечения",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Ваучер"
        verbose_name_plural = "Ваучеры"

    def create_qr_code(self):
        from qr_code.models import VoucherQRCode

        code = VoucherQRCode.objects.create(user=self)
        code.create_code(self.pk, filename=self.pk)
        return code


@receiver(post_save, sender=User)
def create_user_qr_code(sender, instance, created, **kwargs):
    if created:
        instance.create_qr_code()

