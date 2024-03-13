from rest_framework import serializers

from habits.models import GoodHabit
from habits.validators import (HabitsTimeToCompleteValidator, RelatedHabitValidator, HabitsValidator,
                               HabitsPeriodicity, NiceHabitsValidator)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodHabit
        exclude = ['id', 'user']
        validators = [HabitsTimeToCompleteValidator(field='time_to_complete'),
                      RelatedHabitValidator(field='related_habit'),
                      HabitsValidator(field=['related_habit', 'reward']),
                      HabitsPeriodicity(field='periodicity'),
                      NiceHabitsValidator(field=['nice_habits', 'reward'])]
