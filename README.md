# Асинхронный Todo List на FastAPI

Это проект для управления задачами (Todo List), реализованный с использованием **FastAPI** и **SQLAlchemy ORM**. В проекте реализованы функции для создания и удаления пользователей, добавления и удаления задач, а также возможность отмечать задачи как выполненные. Данные хранятся в **PostgreSQL**.

## Описание

Проект позволяет:

- Создавать пользователя
- Добавлять задачи для пользователя
- Удалять задачи (как некоторые так и сразу все)
- Отмечать задачи как выполненные
- Обновлять данные пользователя
- Удалять пользователя (с удалением всех связанных задач)

## Технологии

- **FastAPI** - фреймворк для создания API
- **SQLAlchemy ORM** - для работы с базой данных
- **PostgreSQL** - СУБД для хранения данных
- **Pydantic** - для валидации данных
- **pytest** - для тестирования
- **Alembic** - для миграций базы данных

## API
