from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import Product, ProductCategory, ProductVariation


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    inlines = [ProductVariationInline]


@admin.register(ProductCategory)
class ProductCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name']
