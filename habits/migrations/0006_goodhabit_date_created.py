# Generated by Django 4.2.7 on 2024-03-09 13:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0005_alter_goodhabit_periodicity'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodhabit',
            name='date_created',
            field=models.DateField(auto_now_add=True, default=datetime.date(2024, 3, 9), verbose_name='Дата создания'),
            preserve_default=False,
        ),
    ]
