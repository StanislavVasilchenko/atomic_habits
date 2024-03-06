from django.db import models

from config import settings


class GoodHabit(models.Model):
    HOUR = 'Раз в час'
    WEEK = 'Раз в неделю'
    MONTH = 'РАз в месяц'

    PERIODICITY =[
        (HOUR, 'Раз в час'),
        (WEEK,'Раз в неделю'),
        (MONTH, 'Раз в месяц'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название привычки')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    place = models.CharField(max_length=200, verbose_name='место')
    time = models.TimeField(verbose_name='время выполнения')
    action = models.TextField(verbose_name='действие')
    nice_habit = models.BooleanField(default=False, verbose_name='Признак привычки', blank=True, null=True)
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rel_habit', blank=True,
                                      null=True)
    periodicity = models.CharField(max_length=20, choices=PERIODICITY, verbose_name='переодичность')
    reward = models.TextField(verbose_name='вознаграждение')
    time_to_complete = models.SmallIntegerField(verbose_name='время на выполнение')
    is_published = models.BooleanField(default=False, verbose_name='опубликованно')

    def __str__(self):
        return f'{self.user} - {self.name}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
