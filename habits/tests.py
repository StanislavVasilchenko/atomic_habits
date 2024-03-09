from unittest import TestCase

from django.contrib.auth.models import AnonymousUser
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

    def test_habits_update(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'update_name'
        }

        response = self.client.patch(reverse('habits:habit-update', args=[self.good_habit.id]),
                                     data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), 'update_name')

    def test_habits_update_not_owner(self):
        self.client.force_authenticate(user=self.user_2)

        data = {
            'name': 'update_name'
        }

        response = self.client.patch(reverse('habits:habit-update', args=[self.good_habit.id]),
                                     data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habits_update_reward_with_related_habit(self):
        """При добавлении мвязанной привычки поле вознаграждения становится None"""
        self.client.force_authenticate(user=self.user)

        data = {
            'related_habit': self.nice_habit.id
        }

        response = self.client.patch(reverse('habits:habit-update', args=[self.good_habit.id]),
                                     data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('reward'), None)

    def test_habits_update_good_habit_in_nice_habit(self):
        """При изменении полезной привычки в приятную связаная привычка становится None"""

        self.client.force_authenticate(user=self.user)

        data = {
            'nice_habit': True
        }

        response = self.client.patch(reverse('habits:habit-update', args=[self.good_habit.id]),
                                     data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('related_habit'), None)

    def test_habits_list(self):
        """Список не пубдичных привычек"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('habits:habit-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habits_public_list(self):
        """Список публичных привычек"""
        self.client.force_authenticate(user=self.user_2)

        response = self.client.get(reverse('habits:habit-public-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
