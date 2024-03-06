from rest_framework.exceptions import ValidationError


class HabitsTimeToCompleteValidator:
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        complete_time = value.get('time_to_complete')
        if complete_time > 120:
            raise ValidationError('Time to complete is more than 120 sec')
