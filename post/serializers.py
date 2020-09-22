from rest_framework import serializers

from utils.funcs import get_absolute_url
from .models import Post, PostConfig


class PostListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    first_image = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'short_description', 'first_image', 'content', 'created']

    def get_short_description(self, obj):
        if len(obj.content) < 128:
            return obj.content
        return f'{obj.content[:128]}...'

    def get_first_image(self, obj):
        if obj.images:
            return get_absolute_url(obj.images.all().first().image.url)
        return None

    def get_created(self, obj):
        return obj.created.strftime("%d/%m/%Y")


class PostDetailsSerializer(serializers.ModelSerializer):
    post_images = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_post_images(self, obj):
        if obj.images:
            images = []
            for image in obj.images.all():
                images.append(get_absolute_url(image.image.url))
            return images
        return None

    def get_created(self, obj):
        return obj.created.strftime("%d/%m/%Y")


class PostConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostConfig
        fields = ['show_post_section', 'max_post_amount']
