from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import get_user, change_username, change_email
from app.models import User
from app.security import hash_password



async def create_user(db: AsyncSession, username: str, email: EmailStr, password: str):
    """
    Создание нового пользователя в базе данных.

    Эта функция проверяет, существует ли уже пользователь с таким email. Если да, то генерирует
    ошибку 400. Если email уникален, создается новый пользователь с указанными данными.
    Пароль перед сохранением хешируется. Возвращает созданного пользователя.

    Args:
        db (AsyncSession): Сессия базы данных.
        username (str): Имя пользователя.
        email (EmailStr): Электронная почта пользователя.
        password (str): Пароль пользователя.

    Returns:
        User: Созданный пользователь с хешированным паролем.

    Raises:
        HTTPException:
            - Если пользователь с таким email уже существует (статус 400).
            - Если данные для создания пользователя неверны.
            - Если пользователь с таким именем уже существует (статус 400)
    """
    existing_user = await get_user(db=db, email=email, username=username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с email {email} или именем {username} уже существует.",
        )

    user = User(username=username, email=email, password=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_info(
    db: AsyncSession, user_id: int, new_username: str = None, new_email: EmailStr = None
):
    """
    Обновление информации о пользователе.

    Эта функция обновляет имя и/или email пользователя по переданному user_id.
    Если новый username или email уже заняты другим пользователем, генерируется ошибка 400.
    Если пользователь не найден, генерируется ошибка 404.

    Args:
        db (AsyncSession): Сессия базы данных.
        user_id (int): ID пользователя, информацию о котором нужно обновить.
        new_username (str, optional): Новый username пользователя.
        new_email (EmailStr, optional): Новый email пользователя.

    Returns:
        User: Обновленный пользователь с новыми данными.

    Raises:
        HTTPException:
            - Если пользователь с таким id не найден (статус 404).
            - Если новый username/email уже занят (статус 400).
    """

    user = await get_user(db=db, user_id=user_id)

    if new_username:
        await change_username(db = db, user=user, new_username=new_username
                              )
    if new_email:
        await change_email(db = db, user= user, new_email=new_email)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user_info(db: AsyncSession, user_id: int):
    """
    Получение информации о пользователе по его ID.

    Функция ищет пользователя по его ID и возвращает его данные. Если пользователь не найден,
    генерирует ошибку 404.

    Args:
        db (AsyncSession): Сессия базы данных.
        user_id (int): ID пользователя, чьи данные нужно получить.

    Returns:
        User: Информация о пользователе.

    Raises:
        HTTPException: Если пользователь с таким ID не найден (статус 404).
    """
    user = await get_user(db=db, user_id=user_id)

    return user


async def delete_user(db: AsyncSession, user_id: int):
    """
    Удаление пользователя из базы данных по его ID.

    Функция удаляет пользователя по его ID. Если пользователь не найден, генерируется ошибка 404.

    Args:
        db (AsyncSession): Сессия базы данных.
        user_id (int): ID пользователя, которого нужно удалить.

    Returns:
        dict: Подтверждение успешного удаления пользователя.

    Raises:
        HTTPException: Если пользователь с таким ID не найден (статус 404).
    """
    await get_user(db=db, user_id=user_id)

    await db.execute(delete(User).filter(User.id == user_id))
    await db.commit()

    return {"detail": "Пользователь успешно удален"}
