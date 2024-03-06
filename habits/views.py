from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from habits.models import GoodHabit
from habits.paginators import HabitsPaginator
from habits.permissions import IsHabitOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class HabitDeleteAPIView(generics.DestroyAPIView):
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitOwner]


class GoodHabitListPublicAPIView(generics.ListAPIView):
    queryset = GoodHabit.objects.filter(is_published=True)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
