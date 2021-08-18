## Стек

 Django, MySQL, Django Rest Framework, Django-allauth, djangorestframework-simplejwt, Pipenv, drf-rw-serializers.
 
## Краткое описание: 
Возможность вести блоги авторам. Авторы редактируют свои записи, добавляют, обновляют.
Авторизация по email.

## Запуск
1. Создание виртуального окружения
2. ```pipenv install```
3. Создать базу данных, занести настройки в settings.py
4. Применить миграции
5. ```python manage.py runserver```
6.  Перейти http://127.0.0.1:8000/swagger/