from rest_framework import serializers

from utils.funcs import get_absolute_url
from .models import Post, PostConfig


class PostListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    post_images = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'short_description', 'post_images', 'content', 'created']

    def get_short_description(self, obj):
        if len(obj.content) < 128:
            return obj.content
        return f'{obj.content[:128]}...'

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
