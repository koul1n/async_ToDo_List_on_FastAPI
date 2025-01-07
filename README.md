# Async Todo List

## Описание
Это асинхронное приложение для управления задачами (ToDo List), разработанное с использованием:
- **FastAPI** для создания REST API.
- **SQLAlchemy** для взаимодействия с базой данных.
- **PostgreSQL** в качестве базы данных.
- **Pydantic** для валидации входных данных.
- **Pytest** для тестирования приложения с использованием тестовой базы данных.

## Возможности
### Пользователи:
- Создание нового пользователя.
- Обновление данных пользователя.
- Удаление пользователя (удаляются также все его задачи).

### Задачи:
- Создание задачи для конкретного пользователя.
- Удаление задачи.
- Отметка задачи как выполненной.
- Удаление всех задач пользователя.
- Установка дедлайна для задач.

### Авторизация и аутентификация:
- Использование **JWT токенов** для аутентификации пользователей.
- Генерация токена при входе пользователя.
- Защищенный доступ к маршрутам, требующим авторизации (например, управление задачами).

## Установка

1. Клонируйте репозиторий и перейдите в папку с проектом:
   ```bash
   git clone <URL repository>
   cd <папка с проектом>
   ```

   Структура проекта:
   ```
   .
   ├── app
   │   ├── database
   │   │   ├── __init__.py
   │   │   ├── config.py
   │   │   └── db.py
   │   ├── models
   │   │   ├── __init__.py
   │   │   └── models.py
   │   ├── tasks
   │   │   ├── __init__.py
   │   │   ├── crud.py
   │   │   ├── schemas.py
   │   │   └── tasks_routes.py
   │   └── users
   │       ├── __init__.py
   │       ├── crud.py
   │       ├── schemas.py
   │       └── users_routes.py
   ├── tests
   │   ├── __init__.py
   │   ├── conftest.py
   │   ├── pytest.ini
   │   ├── test_tasks.py
   │   └── test_users.py
   ├── .env
   ├── alembic.ini
   ├── requirements.txt
   ├── run.py
   └── README.md
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Настройте переменные окружения в файле `.env` следующим образом:
   ```env
   DB_DRIVER=postgresql+asyncpg

   DB_USERNAME=<username>
   DB_PASS=<password>
   DB_HOST=<host>
   DB_PORT=<port>
   DB_NAME=<database>

   DB_TEST_USERNAME=<test_username>
   DB_TEST_PASS=<test_password>
   DB_TEST_HOST=<test_host>
   DB_TEST_PORT=<test_port>
   DB_TEST_NAME=<test_database>

   SERVER_HOST=127.0.0.1
   SERVER_PORT=8000
   TESTING=TESTING(заполняем если запускаем на тестовой бд, чтобы поменять зависимость на тестовую бд)
   ```

4. Проведите миграции:
   ```bash
   alembic upgrade head
   ```

5. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Документация API доступна по адресу: [http://localhost:8000/docs](http://localhost:8000/docs).

## Тестирование

Для запуска тестов выполните:
```bash
pytest
```

Тесты выполняются на изолированной тестовой базе данных.

