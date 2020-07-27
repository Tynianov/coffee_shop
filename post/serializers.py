from rest_framework import serializers

from utils.funcs import get_absolute_url
from .models import Post


class PostListSerializer(serializers.ModelSerializer):
    short_content = serializers.SerializerMethodField()
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'short_content', 'first_image']

    def get_short_content(self, obj):
        if len(obj.content) < 128:
            return obj.content
        return f'{obj.content[:128]}...'

    def get_first_image(self, obj):
        if obj.images:
            print('!!!', obj.images.all().first().image)
            return get_absolute_url(obj.images.all().first().image.url)
        return None


class PostDetailsSerializer(serializers.ModelSerializer):
    post_images = serializers.SerializerMethodField()

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
