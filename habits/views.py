from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import GoodHabit
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

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset


class HabitDetailAPIView(generics.RetrieveAPIView):
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    queryset = GoodHabit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsHabitOwner]
