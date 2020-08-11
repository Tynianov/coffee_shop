from rest_framework import serializers
from django.core.paginator import Paginator
from utils.funcs import get_absolute_url
from .models import ProductCategory, Product, ProductVariation


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    variations = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return get_absolute_url(obj.image.url)
        return None

    def get_variations(self, obj):
        qs = obj.variations.active()
        return ProductVariationSerializer(qs, many=True).data

    def get_price(self, obj):
        return obj.variation_min_price


class ProductCategoryListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'image']

    def get_image(self, obj):
        if obj.image:
            return get_absolute_url(obj.image.url)
        return None


class ProductCategoryDetailsSerializer(ProductCategoryListSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ProductCategoryListSerializer.Meta.fields + ["products"]

    def get_products(self, obj):
        return ProductSerializer(obj.products.active(), many=True).data
