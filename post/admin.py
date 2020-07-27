from django.contrib import admin

from .models import PostImage, Post


class PostImageInline(admin.TabularInline):
    model = PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created']
    inlines = [PostImageInline]
