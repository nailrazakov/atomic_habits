from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from habits.serializers import HabitSerializer
from rest_framework.test import APITestCase
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.test")
        self.habit = Habit.objects.create(owner=self.user, place="TEST_PLACE", action="TEST_ACTION", pleasant_habit=False)
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_retrieve(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), self.habit.place)
        self.assertEqual(data.get("action"), "TEST_ACTION")

    def test_habit_create(self):
        url = reverse("habits:habit-list")
        data = {
            "owner": self.user.pk,
            "place": "Дом",
            "action": "Делать приседание",
            "periodicity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {
            "owner": self.user.pk,
            "place": "Где угодно",
            "action": "Петь",
            "periodicity": 1,
        }
        response = self.client.patch(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), "Где угодно")
        self.assertEqual(data.get("action"), "Петь")

    def test_habit_delete(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

# validators test
    def test_pleasant_not_reward_and_related_habit(self):
        """
        Исключает одновременный выбор связанной привычки и указания вознаграждения.
        """
        invalid_data = {
            "owner": self.user.pk,
            "place": "Pleasant",
            "action": "pleasant",
            "reward": "Reward",
            "periodicity": 1,
            "related_habit": "related_habit"
        }
        serializer = HabitSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_time_to_complete_less_120(self):
        """
        Проверка, время выполнения должно быть не больше 120 секунд.
        """
        invalid_data = {
            "owner": self.user.pk,
            "place": "place",
            "action": "action",
            "periodicity": 1,
            "time_to_complete": 121
        }
        serializer = HabitSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_related_habit_only_pleasant(self):
        """
        Проверка, в связанные привычки могут попадать только привычки с признаком приятной привычки.
        """
        print(self.habit.pleasant_habit.__repr__())
        invalid_data = {
            "owner": self.user.pk,
            "place": "place",
            "action": "action",
            "periodicity": 1,
            "related_habit": self.habit
        }
        serializer = HabitSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_pleasant_habit_not_releated_habit(self):
        """
        Проверка, у приятной привычки не может быть вознаграждения или связанной привычки.
        """
        invalid_data = {
            "owner": self.user.pk,
            "place": "place",
            "action": "action",
            "periodicity": 1,
            "pleasant_habit": True,
            "related_habit": self.habit
        }
        serializer = HabitSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_habit_periodicity_over_7(self):
        """
        Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
        """
        invalid_data = {
            "owner": self.user.pk,
            "place": "place",
            "action": "action",
            "periodicity": 8,
        }
        serializer = HabitSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
