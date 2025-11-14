Microblog Service — дипломный проект (Python Advanced, Skillbox)
📌 Описание проекта

Microblog Service — это упрощённый аналог Twitter.
Сервис позволяет:

регистрировать пользователей

создавать твиты

прикреплять к ним медиа

лайкать/дизлайкать твиты

подписываться на других пользователей

просматривать ленту подписок

удалять твиты

удалять лайки

Проект реализован на FastAPI, с использованием:

SQLAlchemy

PostgreSQL

Alembic

Docker + docker-compose

pydantic-схем

Swagger-документации

🧱 Стек технологий
Технология	Использование
Python 3.12	Основной язык
FastAPI	API-сервер
Uvicorn	ASGI-сервер
SQLAlchemy	ORM
PostgreSQL	База данных
Alembic	Миграции
Docker / docker-compose	Контейнеризация
pydantic	Валидация данных
Swagger UI	Документация API
git clone <ссылка на ваш GitHub репозиторий>
cd Python_advanced_diplom


🚀 Запуск проекта
1. Клонировать репозиторий:
git clone <ссылка на ваш GitHub репозиторий>
cd Python_advanced_diplom

2. Создать файл .env в корне проекта:
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=postgres
k1=User k1
k2=User k2

3. Запустить проект:
docker-compose up --build

4. Открыть Swagger UI:
http://localhost:8000/docs


📁 Структура проекта
app/
 ├── models/
 ├── routers/
 ├── schemas/
 ├── crud.py
 ├── database.py
 ├── config.py
 ├── main.py
alembic/
Diplom/
 ├── Скриншоты (11 файлов)
docker-compose.yml
Dockerfile
README.md


📝 Выполненные пункты задания
✔ Пользователь k1

авторизация
просмотр профиля
просмотр профиля k2
лайк твита
удаление лайка
просмотр ленты (до и после удаления твита)

✔ Пользователь k2
регистрация
загрузка медиа
создание твита
удаление твита

📎 Скриншоты (см. папку Diplom)

Регистрация пользователя k1
Авторизация под k1
Авторизация под k2
Загрузка медиа k2
Создание твита k2
Лайк твита k1
Просмотр ленты k1
Просмотр профиля k2 от имени k1
Просмотр профиля k1 от имени k2
Удаление лайка
Удаление твита
Лента после удаления твита

📦 Завершение
Проект полностью реализует техническое задание Skillbox.
Swagger-документация доступна по адресу:
http://localhost:8000/docs