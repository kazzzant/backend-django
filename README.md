# Интернет магазин

Проект написан по уже готовому шаблону фронта. Backend разработан на фреймворке Django. 
Получение данных происходит по API, который реализован с использованием Django Rest Framework.

## Структура проекта

Проект состит из следующих приложений:
- myauth - обработка данных о пользователе;
- shopapp - товары магазина;
- cart - корзина для храния товаров;


## Документация:
- README.md - описание проекта;
- requirements.txt - файл зависимостей;


## Для запуска проекта нужно:
1. Установить зависимости, указанные в файле `requirements.txt`.
2. Перейти в папку с проектом командой `cd megano`
3. Применить миграции командой `python manage.py makemigrations`
4. Запустить сервер командой `python manage.py runserver`
