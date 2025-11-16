from datetime import timedelta
from rest_framework.exceptions import ValidationError


class ChoiceRewardValidator:
    """Исключает одновременный выбор связанной привычки и указания вознаграждения."""

    def __init__(self, related_habit, reward):
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, habit):
        if habit.get(self.related_habit) and habit.get(self.reward):
            raise ValidationError(
                f"""Вы не можете одновременно выбрать {self.related_habit} и {self.reward} ,выберите что-то одно."""
            )


class TimeValidator:
    """Проверка, время выполнения должно быть не больше 120 секунд."""

    def __init__(self, time_to_complete):
        self.time_to_complete = time_to_complete

    def __call__(self, habit):
        time_to_complete_end = timedelta(minutes=2)
        if (
            habit.get(self.time_to_complete)
            and habit.get(self.time_to_complete) > time_to_complete_end
        ):
            raise ValidationError(
                f"Время выполнения не может быть более {time_to_complete_end} минут."
            )


class RelatedHabitValidator:
    """Проверка, в связанные привычки могут попадать только привычки с признаком приятной привычки."""

    def __call__(self, habit):
        related_habit = habit.get("related_habit")
        if related_habit and not related_habit.pleasant_habit:
            raise ValidationError("Связанная привычка не является приятной.")


class PeriodicityValidator:
    """Проверяет, является ли периодичность привычки корректной."""

    def __init__(self, periodicity):
        self.periodicity = periodicity

    def __call__(self, habit):
        if habit.get(self.periodicity) not in range(1, 8):
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")


class NoConnectionValidator:
    """Проверка, у приятной привычки не может быть вознаграждения или связанной привычки."""

    def __init__(self, pleasant_habit, related_habit, reward):
        self.pleasant_habit = pleasant_habit
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, habit):
        if habit.get(self.pleasant_habit):
            if habit.get(self.reward) or habit.get(self.related_habit):
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )
