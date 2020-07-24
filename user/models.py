from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    instagram_username = models.CharField(
        "Профиль в Instagram",
        max_length=30,
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        "Номер телефона",
        max_length=16,
        null=True,
        blank=True
    )
    email = models.EmailField(
        "Адрес электронной почты",
        max_length=255,
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'last_name', 'first_name', 'username']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def create_qr_code(self):
        from qr_code.models import UserQRCode

        code = UserQRCode.objects.create(user=self)
        code.create_code(self.pk, filename=self.email)
        return code


# @receiver(post_save, sender=User)
# def create_user_qr_code(sender, instance, created, **kwargs):
#     if created:
#         if not hasattr(instance, 'qr_code'):
#             instance.create_qr_code()
