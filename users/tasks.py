from celery import shared_task

from users.models import User
from users.services import get_telegram_id, save_user_telegram_id


@shared_task
def save_tg_id_in_user():
    telegram_id = get_telegram_id()
    for data in telegram_id.json().get('result'):
        if data.get('message') is not None:
            user_name = data.get('message')['from'].get('username')
            user_id = data.get('message')['from']['id']
            print(f'user_name: {user_name}, user_id: {user_id}', end=' ')
            try:
                user = User.objects.get(telegram_username=user_name, telegram_id__isnull=False)
                save_user_telegram_id(user, user_id)
            except User.DoesNotExist:
                pass
