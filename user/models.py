from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to='users/profile_images',
        null=True,
    )
    qr_code = models.ImageField(
        upload_to='users/qr_codes',
    )
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
