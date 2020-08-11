from django.contrib import admin

from .models import Product, ProductCategory, ProductVariation


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    inlines = [ProductVariationInline]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
