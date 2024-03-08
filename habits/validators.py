from rest_framework.exceptions import ValidationError


class HabitsTimeToCompleteValidator:
    """Валидатор для времени выполнения. Время выполнения не должно быть больше 120 секунд"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        complete_time = value.get('time_to_complete')
        if complete_time is not None and complete_time > 120:
            raise ValidationError('Время выполнение не должно быть больше 120 sec')


class RelatedHabitValidator:
    """Валидатор для связанной привычки. У связанной привычки должен быть признак приятной привычки"""

    def __init__(self, field):
        self.fields = field

    def __call__(self, value):
        related_habit = value.get('related_habit')
        if related_habit is not None and not related_habit.nice_habit:
            raise ValidationError('Связаной привычкой может быть только приятная привычка')


class HabitsValidator:
    """Валидатор для Полезной привычки. Нельзя выбрать одновременно связанную привычку и вознаграждение"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reward = value.get('reward')
        related_habit = value.get('related_habit')
        if reward is not None and related_habit is not None:
            raise ValidationError('У привычки не может быть вознаграждения и приятной привычки ')
