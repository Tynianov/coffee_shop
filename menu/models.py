from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from utils.models import StatusModel, StatusQuerySet


class ProductCategory(StatusModel):
    name = models.CharField(
        _("Category name"),
        max_length=128
    )
    image = models.ImageField(
        upload_to='categories/images'
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    objects = StatusQuerySet.as_manager()


class Product(StatusModel):
    name = models.CharField(
        _("Product name"),
        max_length=128
    )
    description = models.TextField(
        _("Product description"),
        null=True,
        blank=True
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )
    image = models.ImageField(
        upload_to='products/images'
    )

    objects = StatusQuerySet.as_manager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.name}, {self.category.name}"

    @property
    def variation_min_price(self):
        if not self.variations.active().exists():
            return self.price
        return min(list(self.variations.active().values_list('price', flat=True)))


class ProductVariation(StatusModel):
    name = models.CharField(
        _("Name"),
        max_length=128
    )
    price = models.DecimalField(
        _('Price'),
        decimal_places=2,
        max_digits=5
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variations'
    )

    objects = StatusQuerySet.as_manager()

    class Meta:
        verbose_name = _("Product Variation")
        verbose_name_plural = _("Product Variations")

    def __str__(self):
        return f'{self.name} - {self.product.name}'
