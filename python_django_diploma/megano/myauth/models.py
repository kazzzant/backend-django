from django.contrib.auth.models import User
from django.db import models


class Avatar(models.Model):
    """Модель для хранения аватара пользователя"""

    src = models.ImageField(
        upload_to="avatars/",
        default="avatars/default.png",
        verbose_name="Ссылка",
    )
    alt = models.CharField(default="avatar", max_length=128, verbose_name="Описание")

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"


class Profile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(blank=False, max_length=128, verbose_name="Полное имя")
    email = models.EmailField(
        blank=False, unique=True, max_length=128, verbose_name="e-mail"
    )
    phone = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="Номер телефона"
    )
    avatar = models.ForeignKey(
        Avatar,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="profile",
        verbose_name="Аватар",
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.fullName} ({self.user})({self.id})"
