from django.db import models

from utils.models import StatusModel
# Create your models here.


class ProductCategory(StatusModel):
    name = models.CharField(
        "Имя категории",
        max_length=128
    )
    image = models.ImageField(
        upload_to='categories/images'
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(StatusModel):
    name = models.CharField(
        "Название продукта",
        max_length=128
    )
    description = models.CharField(
        "Описание продукта",
        max_length=256,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        "Цена",
        max_digits=8,
        decimal_places=2,
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products/images'
    )
