from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):  # Пользователь приложения
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите ваш Email"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите ваш аватар"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        **NULLABLE,
        help_text="Укажите ваш номер телефона"
    )
    tg_nick = models.CharField(
        max_length=50,
        verbose_name="Ник телеграмм",
        help_text="Укажите ваше имя в телеграмме",
        **NULLABLE
    )
    tg_chat_id = models.CharField(max_length=50, verbose_name="Телеграм chat-id",
                                  help_text="Укажите телеграм chat-id", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
