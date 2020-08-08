from rest_framework import serializers

from utils.funcs import get_absolute_url
from .models import ProductCategory, Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return get_absolute_url(obj.image.url)
        return None


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
