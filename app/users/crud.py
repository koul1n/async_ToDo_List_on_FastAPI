from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User
from app.security import hash_password


async def get_user(
    *,
    db: AsyncSession,
    email: EmailStr = None,
    user_id: int = None,
    username: str = None,
):
    """
    Получение пользователя из базы данных.

    Эта функция позволяет получить пользователя по одному из переданных параметров:
    email, user_id или username. Если ни один параметр не указан, возвращается None.

    Параметры:
    - db (AsyncSession): Асинхронная сессия базы данных.
    - email (EmailStr, optional): Email пользователя. Если указан, поиск производится по email.
    - user_id (int, optional): Идентификатор пользователя. Если указан, поиск производится по user_id.
    - username (str, optional): Имя пользователя. Если указано, поиск производится по username.

    Возвращает:
    - User: Найденный пользователь или None, если пользователь не найден или параметры не указаны.

    Примечание:
    - Если указано несколько параметров (email, user_id, username), используется только первый из них.
    - При отсутствии всех параметров возвращается None.
    """
    if email:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    elif user_id:
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
    elif username:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    return None


async def get_user_by_email(db: AsyncSession, email: EmailStr):
    """
    Получение пользователя из базы данных по его email.

    Функция ищет пользователя в базе данных по переданному email. Если пользователь с таким
    email найден, возвращает его данные. В противном случае генерирует ошибку 404.

    Args:
        db (AsyncSession): Сессия базы данных.
        email (EmailStr): Электронная почта пользователя.

    Returns:
        User: Пользователь, найденный по email.

    Raises:
        HTTPException: Если пользователь с таким email не найден (статус 404).
    """
    user = await get_user(db=db, email=email)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Пользователь с email {email} не существует.",
    )


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

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден."
        )

    if new_username:

        existing_user = await get_user(db=db, username=new_username)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь с именем {new_username} уже существует.",
            )
        user.username = new_username

    if new_email:
        existing_user = await get_user(db=db, email=new_email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь с email {new_email} уже существует.",
            )
        user.email = new_email

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
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден."
        )
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
    user = await get_user(db=db, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден."
        )

    await db.execute(delete(User).filter(User.id == user_id))
    await db.commit()

    return {"detail": "Пользователь успешно удален"}
