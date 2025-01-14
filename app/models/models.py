from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

"""
Модуль для определения моделей базы данных с использованием SQLAlchemy.

Этот модуль содержит модели для пользователей и задач, которые используются
для создания таблиц в базе данных. Каждая модель включает в себя поля, соответствующие
данным, и устанавливает связи между моделями.
"""


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей, который наследует от `DeclarativeBase`.

    Все модели должны наследовать этот класс для правильной работы с SQLAlchemy.
    """

    pass


class Task(Base):
    """
    Модель задачи.

    Атрибуты:
        id (int): Уникальный идентификатор задачи.
        title (str): Заголовок задачи.
        description (str): Описание задачи.
        is_completed (bool): Статус завершённости задачи.
        created_at (datetime): Дата и время создания задачи.
        deadline (datetime | None): Дедлайн задачи (если есть).
        owner_id (int): Идентификатор владельца задачи (внешний ключ).
        owner (User): Связь с пользователем, который является владельцем задачи.

    Связи:
        owner (User): Один пользователь может иметь несколько задач.
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(nullable=True)

    # Ссылка на пользователя
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="tasks")


class User(Base):
    """
    Модель пользователя.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        username (str): Уникальное имя пользователя.
        email (str): Уникальная электронная почта пользователя.
        password (str): Пароль пользователя.
        is_active (bool): Статус активности пользователя.

    Связи:
        tasks (list[Task]): Список задач пользователя.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Связь с задачами
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="owner", cascade="all, delete"
    )
