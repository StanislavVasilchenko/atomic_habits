from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import GoodHabit
from users.models import User


class HabitsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@test.ru',
            password='12345'
        )

        self.user_2 = User.objects.create(
            email='test2@test2.com',
            password='54321'
        )

        self.good_habit = GoodHabit.objects.create(
            name='test',
            user=self.user,
            place='Home test',
            time='12:00:00',
            action='Test action',
            reward='Test reward',
            time_to_complete=20,

        )

        self.nice_habit = GoodHabit.objects.create(
            name='test2',
            user=self.user,
            place='Home test2',
            time='12:00:00',
            action='Test action2',
            reward='Test reward2',
            time_to_complete=20,
            nice_habit=True,
        )

    def test_habits_create(self):
        """Тест создания привычки"""
        self.client.force_authenticate(user=self.user)

        data = {
            'name': self.good_habit.name,
            'place': self.good_habit.place,
            'time': self.good_habit.time,
            'action': self.good_habit.action,
            'user': self.user,
            'reward': self.good_habit.reward,
            'time_to_complete': self.good_habit.time_to_complete
        }

        response = self.client.post(
            reverse('habits:habit-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habits_create_with_nice_habit(self):
        """Тест для создания привычки со связанной приятной привычкой"""
        self.client.force_authenticate(user=self.user)

        data = {
            'name': self.good_habit.name,
            'place': self.good_habit.place,
            'time': self.good_habit.time,
            'action': self.good_habit.action,
            'user': self.user,
            'reward': self.good_habit.reward,
            'time_to_complete': self.good_habit.time_to_complete,
            'related_habit': self.nice_habit.id
        }

        response = self.client.post(reverse('habits:habit-create'),
                                    data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': ['У привычки не может быть вознаграждения и приятной привычки']})

    def test_habits_with_nice_habit_false(self):
        """Связанной привычкой может быть только приятная привычка"""
        self.client.force_authenticate(user=self.user)

        data = {
            'name': self.good_habit.name,
            'place': self.good_habit.place,
            'time': self.good_habit.time,
            'action': self.good_habit.action,
            'user': self.user,
            'time_to_complete': self.good_habit.time_to_complete,
            'related_habit': self.good_habit.id
        }

        response = self.client.post(reverse('habits:habit-create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': ['Связаной привычкой может быть только приятная привычка']})

    def test_habits_create_time(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'name': self.good_habit.name,
            'place': self.good_habit.place,
            'time': self.good_habit.time,
            'action': self.good_habit.action,
            'user': self.user,
            'time_to_complete': 121,
        }

        response = self.client.post(reverse('habits:habit-create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': ['Время выполнение не должно быть больше 120 sec']})

    def test_habits_periodicity(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'name': self.good_habit.name,
            'place': self.good_habit.place,
            'time': self.good_habit.time,
            'action': self.good_habit.action,
            'user': self.user,
            'time_to_complete': 120,
            'periodicity': 8
        }

        response = self.client.post(reverse('habits:habit-create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': ['Переиодичность не должна привышать 7 дней']})
