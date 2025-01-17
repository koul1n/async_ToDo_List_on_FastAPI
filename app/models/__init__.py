"""
Модуль для определения моделей базы данных с использованием SQLAlchemy.

Этот модуль содержит модели для пользователей и задач, которые используются
для создания таблиц в базе данных. Каждая модель включает в себя поля, соответствующие
данным, и устанавливает связи между моделями.
"""

from .models import Base, Task, User
