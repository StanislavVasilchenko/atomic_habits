from rest_framework import serializers

from habits.models import GoodHabit
from habits.validators import HabitsTimeToCompleteValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodHabit
        exclude = ['id', 'user']
        validators = [HabitsTimeToCompleteValidator(fields='time_to_complete')]
