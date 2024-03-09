from datetime import datetime, timedelta

import requests
from celery import shared_task

from habits.models import GoodHabit
from private_keys import TG_TOKEN


@shared_task
def telegram_notification():
    """Отправляет напоминание пользователюв телеграмм о привычках, которые необходимо выполнить.
    После отправки напоминания перезаписывает дату следующего выполнения"""
    url = 'https://api.telegram.org/bot'
    token = TG_TOKEN
    time_now = datetime.now().time().strftime('%H:%M')
    date_now = datetime.now().date().strftime('%Y-%m-%d')

    habits = GoodHabit.objects.filter(time=time_now, nice_habit=False, date_of_completion=date_now)

    if habits:
        for habit in habits:
            response = requests.post(url=f'{url}{token}/sendMessage',
                                     data={
                                         'chat_id': habit.user.telegram_id,
                                         'text': f'Вам необходимо выполнить свою привычку {habit.name} в {habit.time} '
                                                 f'Место - {habit.place} '
                                                 f'Действие - {habit.action}'
                                     }
                                     )
            habit.date_of_completion += timedelta(days=habit.periodicity)
            habit.save()
