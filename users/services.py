import requests

from private_keys import TG_TOKEN
from users.models import User


def get_telegram_id():
    url = 'https://api.telegram.org/bot'
    token = TG_TOKEN
    response = requests.get(url=f'{url}{token}/getUpdates')
    return response


def save_user_telegram_id(user: User, user_id: str) -> None:
    user.telegram_id = user_id
    user.save()
