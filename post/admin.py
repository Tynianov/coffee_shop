from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import PostImage, Post, PostConfig


class PostImageInline(admin.TabularInline):
    model = PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created']
    inlines = [PostImageInline]


@admin.register(PostConfig)
class PostConfigAdmin(SingletonModelAdmin):
    pass
