# Learning Management System API

## Описание

Это API для системы управления обучением, которое позволяет управлять данными 
о курсах, уроках и учениках. API реализован на основе стека Django REST Framework, PostgreSQL и Celery.

## Требования

- Python 3.6 или выше
- Django 4.2(не выше 5)
- Django REST Framework 3.12 или выше
- PostgreSQL 16 или выше
- Celery 5.0 или выше

## Установка

1. Склонируйте репозиторий на свой компьютер:
```commandline
git clone https://github.com/InsatiateDevil/lms-drf
```

2. Перейдите в директорию проекта:
```commandline
cd lms-drf
```

3. Активируйте окружение и установите зависимости:
```commandline
pip install -r requirements.txt
```


## Использование

1. Запустите сервер Django:
```commandline
python manage.py runserver
```

2. Откройте браузер и перейдите по адресу http://127.0.0.1:8000/swagger-ui/,
чтобы получить доступ к документации API.
