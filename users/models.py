from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email address')
    telegram_id = models.IntegerField(verbose_name='Telegram')
    phone_number = models.CharField(max_length=15, verbose_name='telephone number')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
