from datetime import timedelta

from django.db import models
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):  # Привычка
    owner = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE, **NULLABLE
    )
    place = models.TextField(
        verbose_name="Место", help_text="Укажите место выполнения привычки"
    )
    time = models.TimeField(
        verbose_name="Время", help_text="Укажите время выполнения привычки", **NULLABLE
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Укажите действие, которое представляет собой привычка",
    )
    pleasant_habit = models.BooleanField(
        default=True,
        verbose_name="Признак приятной привычки",
        help_text="Привычка, которую можно привязать к выполнению полезной привычки",
        **NULLABLE,
    )
    related_habit = models.ForeignKey(
        "self", verbose_name="Связанная привычка", on_delete=models.CASCADE, **NULLABLE
    )
    periodicity = models.IntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Укажите периодичность выполнения привычки(по умолчанию ежедневная)",
    )
    reward = models.CharField(
        max_length=150,
        verbose_name="Вознаграждение",
        help_text="Укажите, чем хотите себя вознаградить после выполнения",
        **NULLABLE,
    )
    time_to_complete = models.DurationField(
        verbose_name="Время на выполнение",
        help_text="Время, которое предположительно потратите",
        default=timedelta(seconds=120),
        **NULLABLE,
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Опубликовать для общего доступа",
        **NULLABLE,
    )

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
