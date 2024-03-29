from rest_framework.exceptions import ValidationError


class HabitsValidatorMixin:
    def __init__(self, field):
        self.field = field


class HabitsTimeToCompleteValidator(HabitsValidatorMixin):
    """Валидатор для времени выполнения. Время выполнения не должно быть больше 120 секунд"""

    def __call__(self, value):
        complete_time = value.get('time_to_complete')
        if complete_time is not None and complete_time > 120:
            raise ValidationError('Время выполнение не должно быть больше 120 sec')


class RelatedHabitValidator(HabitsValidatorMixin):
    """Валидатор для связанной привычки. У связанной привычки должен быть признак приятной привычки"""

    def __call__(self, value):
        related_habit = value.get('related_habit')
        if related_habit is not None and not related_habit.nice_habit:
            raise ValidationError('Связаной привычкой может быть только приятная привычка')


class HabitsValidator(HabitsValidatorMixin):
    """Валидатор для Полезной привычки. Нельзя выбрать одновременно связанную привычку и вознаграждение"""

    def __call__(self, value):
        reward = value.get('reward')
        related_habit = value.get('related_habit')
        if reward is not None and related_habit is not None:
            raise ValidationError('У привычки не может быть вознаграждения и приятной привычки')


class HabitsPeriodicity(HabitsValidatorMixin):
    """ Валидатор для проверки периодичносит выполнения привычки. Не может привышать 7 дней"""

    def __call__(self, value):
        periodicity = value.get('periodicity')
        if periodicity is not None and periodicity > 7:
            raise ValidationError('Переиодичность не должна привышать 7 дней')


class NiceHabitsValidator(HabitsValidatorMixin):
    """Валидатор для приятной привычки. У приятной привычки не должно быть поля вознаграждения (reward)"""

    def __call__(self, value):
        nice_habit = value.get('nice_habit')
        reward = value.get('reward')
        if nice_habit and reward:
            raise ValidationError('У приятной привычки не может быть вознаграждения')
