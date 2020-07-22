from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to='users/profile_images',
        null=True,
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
