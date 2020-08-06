from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel

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
    content = models.TextField(
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


class PostConfig(SingletonModel):
    show_post_section = models.BooleanField(
        _("Show post section in app?"),
        default=True
    )
    max_post_amount = models.PositiveSmallIntegerField(
        _("How much post to show in mobile app?"),
        default=5,
        help_text=_("Set how much post to show in mobile app. "
                    "Rest of the post will be visible after clicking 'more' button")
    )

    class Meta:
        verbose_name = _("Posts config")
