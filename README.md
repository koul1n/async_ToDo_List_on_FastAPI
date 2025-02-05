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
- Обновление задач.

### Авторизация и аутентификация:
- Использование **JWT токенов** для аутентификации пользователей.
- Генерация токена при входе пользователя.
- Защищенный доступ к маршрутам, требующим авторизации (например, управление задачами).

## Установка

1. Клонируйте репозиторий и перейдите в папку с проектом:
   ```bash
   git clone https://github.com/koul1n/async_ToDo_List_on_FastAPI.git
   cd async_ToDo_List_on_FastAPI
   ```

   ## Структура проекта:

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
│   ├── security
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── schemas.py
│   │   └── utils.py
│   ├── logs
│   │   ├── __init__.py
│   │   ├── service.py
│   │   
│   ├── tasks
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── schemas.py
│   │   └── tasks_routes.py
│   ├── users
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── schemas.py
│   │   └── users_routes.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── pytest.ini
│   ├── test_tasks.py
│   └── test_users.py
├── .dockerignore
├── .env
├── .flake8
├── alembic.ini
├── docker-compose.yml
├── docker-entrypoint.sh
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── run.py
└── README.md

   ```

2. Запустите команду:
   ```bash
   docker-compose up --build
   ```


3. Документация API доступна если перейти на: [/docs](/docs).

## Тестирование

Для запуска тестов выполните:
```bash
docker exec -it todolist pytest
```



