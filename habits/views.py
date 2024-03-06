from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import GoodHabit
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    queryset = GoodHabit
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)