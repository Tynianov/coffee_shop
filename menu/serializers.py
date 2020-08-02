from rest_framework import serializers

from utils.funcs import get_absolute_url
from .models import ProductCategory, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def get_image(self, obj):
        return get_absolute_url(obj.image.url)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


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
