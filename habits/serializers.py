from rest_framework import serializers

from habits.models import GoodHabit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodHabit
        exclude = ['id', 'user']
