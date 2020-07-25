from django.db import models


class StatusModel(models.Model):
    is_active = models.BooleanField(
        "Активен?",
        default=True,
        db_index=True,
        help_text="Отметьте, если объект должен быть активным"
    )

    class Meta:
        abstract = True


class StatusQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
