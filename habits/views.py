from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.models import GoodHabit
from habits.paginators import HabitsPaginator
from habits.permissions import IsHabitOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """При создании привязывается авторизованный пользователь.
        Если привычка приятная поле вознаграждения очищается"""
        new_habit = serializer.save(user=self.request.user)
        if new_habit.nice_habit:
            new_habit.reward = None
            new_habit.save()


class HabitListAPIView(generics.ListAPIView):
    """Вывод списка всех привычек"""
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPaginator

    def get_queryset(self):
        """Фильтр для вывода привычек автоизованного пользователя"""
        queryset = self.queryset.filter(user=self.request.user)
        return queryset.order_by('-id')


class HabitDetailAPIView(generics.RetrieveAPIView):
    """Информация об одной привычки"""
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Обновление данных привычки"""
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitOwner]

    def perform_update(self, serializer):
        """Обновление полей related_habit и nice_habit.
        Если у привычки есть связанная приятная привычка поле вознаграждения очищается.
        Если полезную привычку перевести в статус приятной то очищаетяс поле связанной привычки"""
        updated_habit = serializer.save()
        if updated_habit.related_habit:
            updated_habit.reward = None
        if updated_habit.nice_habit:
            updated_habit.related_habit = None
        updated_habit.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class HabitDeleteAPIView(generics.DestroyAPIView):
    """Удаление привычки"""
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitOwner]


class GoodHabitListPublicAPIView(generics.ListAPIView):
    """Вывод списка публичных привычек"""
    queryset = GoodHabit.objects.filter(is_published=True)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
