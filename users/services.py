import requests

from private_keys import TG_TOKEN


def get_telegram_id():
    url = 'https://api.telegram.org/bot'
    token = TG_TOKEN
    response = requests.get(url=f'{url}{token}/getUpdates')
    return response
