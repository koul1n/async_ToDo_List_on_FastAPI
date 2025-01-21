"""
Этот файл содержит модели SQLAlchemy для работы с задачами и пользователями.
Модели описывают структуру таблиц в базе данных и связи между ними. Модель Task используется для представления задач,
включая их статус и владельца. Модель User используется для хранения информации о пользователях, включая их задачи.

Основные компоненты:
    - Base: Базовый класс для всех моделей данных с использованием SQLAlchemy.
    - Task: Модель для задач с атрибутами, такими как заголовок, описание, статус и дедлайн.
    - User: Модель для пользователей с атрибутами, такими как имя пользователя, электронная почта и пароль.

    Связи между моделями:
        - Каждая задача связана с одним пользователем (владельцем).
        - Каждый пользователь может иметь несколько задач.
"""

from datetime import datetime
from app.tasks.schemas import TaskStatus
from sqlalchemy import ForeignKey, func, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    Атрибуты:
        id (int): Уникальный идентификатор.
    Базовый класс для всех моделей данных.

    """

    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class Task(Base):
    """
    Модель для задачи.

    Атрибуты:
        id (int): Уникальный идентификатор задачи (наследуется от Base).
        title (str): Заголовок задачи.
        description (str): Описание задачи.
        status (TaskStatus): Статус задачи (например, NEW).
        created_at (datetime): Дата и время создания задачи.
        deadline (datetime | None): Дедлайн задачи.
        owner_id (int): Идентификатор пользователя, который является владельцем задачи.
        owner (User): Связь с пользователем, владельцем задачи.

    Связи:
        - Связана с пользователем через поле owner_id.
    """

    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.NEW, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(nullable=True)

    # Ссылка на пользователя
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="tasks")


class User(Base):
    """
    Модель для пользователя.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя (Наследуется от Base).
        username (str): Имя пользователя.
        email (str): Электронная почта пользователя.
        password (str): Пароль пользователя.
        is_active (bool): Статус активности пользователя.

    Связи:
        - Пользователь может иметь несколько задач (связь с моделью Task).
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Связь с задачами
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="owner", cascade="all, delete"
    )
