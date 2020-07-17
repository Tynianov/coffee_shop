from django.db import models

from utils.models import StatusModel


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
        "Выберете",
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
