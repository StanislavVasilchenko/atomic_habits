from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.models import GoodHabit
from habits.paginators import HabitsPaginator
from habits.permissions import IsHabitOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save(user=self.request.user)
        if new_habit.nice_habit:
            new_habit.reward = None
            new_habit.save()


class HabitListAPIView(generics.ListCreateAPIView):
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPaginator

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset.order_by('-id')


class HabitDetailAPIView(generics.RetrieveAPIView):
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitOwner]

    def perform_update(self, serializer):
        updated_habit = serializer.save()
        if updated_habit.related_habit:
            updated_habit.reward = None
        if updated_habit.nice_habit:
            updated_habit.related_habit = None
        updated_habit.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class HabitDeleteAPIView(generics.DestroyAPIView):
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitOwner]


class GoodHabitListPublicAPIView(generics.ListAPIView):
    queryset = GoodHabit.objects.filter(is_published=True)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
