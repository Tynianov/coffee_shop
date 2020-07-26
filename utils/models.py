from django.db import models
from django.utils.translation import ugettext_lazy as _


class StatusModel(models.Model):
    is_active = models.BooleanField(
        _("Is active?"),
        default=True,
        db_index=True,
        help_text=_("Designate, if object is active")
    )

    class Meta:
        abstract = True


class StatusQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
