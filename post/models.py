from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField as HTMLField

from utils.models import StatusQuerySet, StatusModel


class PostImage(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        _("Post image"),
        upload_to='post/images'
    )

    class Meta:
        verbose_name = _("Post image")
        verbose_name_plural = _("Post images")


class Post(StatusModel):
    title = models.CharField(
        _("Title"),
        max_length=128
    )
    content = HTMLField(
        _("Post content")
    )
    created = models.DateTimeField(
        _("Creation date"),
        auto_now_add=True
    )

    objects = StatusQuerySet.as_manager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ["-created"]
