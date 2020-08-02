from django.db import models
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
    description = models.CharField(
        _("Product description"),
        max_length=256,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=8,
        decimal_places=2,
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )

    objects = StatusQuerySet.as_manager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.name}, {self.category.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products/images'
    )
