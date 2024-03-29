import os

from dotenv import load_dotenv

load_dotenv()

DJANGO_KEY = os.getenv('DJANGO_KEY')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')

BROKER_URL = os.getenv('BROKER_URL')
RESULT_BACKEND = os.getenv('RESULT_BACKEND')

TG_TOKEN = os.getenv('TG_TOKEN')
