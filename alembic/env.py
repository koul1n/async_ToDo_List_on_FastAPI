from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.models import Base
from app.database import settings


DATABASE_URL = settings.dsn()

DATABASE_TEST_URL = settings.dsn_for_test()

# Устанавливаем конфигурацию
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные для автогенерации
target_metadata = Base.metadata

def run_migrations_offline():
    """Запуск миграций в оффлайн-режиме."""
    url = DATABASE_TEST_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запуск миграций в онлайн-режиме (асинхронно)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    try:
        # Подключаемся асинхронно к базе данных
        async with connectable.connect() as connection:
            # Выполнение миграции с использованием синхронного метода
            await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(f"Error running migrations: {e}")
    finally:
        # Закрываем соединение
        await connectable.dispose()


def do_run_migrations(connection):
    """Функция для выполнения миграций."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,  # Если нужно делать изменения с SQLite
    )

    with context.begin_transaction():
        context.run_migrations()


# Проверка режима работы
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    # Асинхронно выполняем миграции
    asyncio.run(run_migrations_online())
