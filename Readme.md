# Atomic Habit
Атомные привычки. Бэкенд для Django позволет создать список привычек с периодичностью выполнения. Интеграция с Телеграмм ботом для отправки напоминания о времени выполнения и описанием выполнения (Необходимо создать бота и получить API ключ).

## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Тестирование](#тестирование)


## Технологии
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Celery beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
- [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/)
- [CORS](https://pypi.org/project/django-cors-headers/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

## Использование


Создание базу данных postgres:
```
CREATE DATABASE db_name
```
Создать .env фаил:
```
Пример заполнения в файле .env.sample
```
Запуск celery worker для отправки уведомлений в Телеграмм:
```
celery --A config worker --loglevel=info
```
Запуск celery beat для отслеживания времени выполннени привычки:
```
celery --A config beat --loglevel=info
```

## Разработка

### Требования
Для установки и запуска проекта, необходим [NodeJS](https://nodejs.org/) v8+.

### Установка зависимостей
Для установки зависимостей, выполните команду:
```
pip install requirements.txt
```

### Запуск сервера
Чтобы запустить сервер :
```
python3 manage.py runserver
```


## Тестирование

Проект покрыт юнит-тестами. Для их запуска выполните команду:
```
python3 manage.py test  
```
м-то вдохновлялись, расскажите об этом: где брали идеи, какие туториалы смотрели, ссылки на исходники кода. 