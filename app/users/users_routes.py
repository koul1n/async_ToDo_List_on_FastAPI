from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import database_helper
from app.security import TokenInfo, create_jwt, get_current_user, validate_password
from app.users import (
    UserCreate,
    UserResponse,
    UserUpdate,
    create_user,
    delete_user,
    get_user_by_email,
    get_user_info,
    update_user_info,
)

router = APIRouter(prefix="/api/v1/users")


@router.post("/login/", response_model=TokenInfo)
async def login_route(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database_helper.get_db),
):
    """
    Авторизация пользователя с использованием email и пароля.

    Этот маршрут обрабатывает запрос на вход в систему. Он принимает данные формы
    с email (в качестве имени пользователя) и паролем, проверяет их, и если данные корректны,
    генерирует JWT токен для аутентификации.

    Args:
        form_data (OAuth2PasswordRequestForm): Данные для входа в систему (email и пароль).
        db (AsyncSession): Сессия базы данных для взаимодействия с пользователями.

    Raises:
        HTTPException: В случае некорректных данных для входа (неправильный пароль или email).

    Returns:
        TokenInfo: JWT токен для аутентификации пользователя.
    """
    user = await get_user_by_email(db=db, email=form_data.username)

    if user and validate_password(pwd=form_data.password, hashed_pwd=user.password):
        token = create_jwt({"sub": user.id, "username": user.username})
        return TokenInfo(access_token=token, token_type="Bearer")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )


@router.post("/register/", response_model=UserResponse)
async def create_user_route(
    user: UserCreate, db: AsyncSession = Depends(database_helper.get_db)
):
    """
    Регистрация нового пользователя.

    Этот маршрут позволяет создать нового пользователя в системе. При этом проверяется,
    существует ли уже пользователь с таким email. Если пользователь существует, возвращается ошибка.

    Args:
        user (UserCreate): Данные пользователя для регистрации.
        db (AsyncSession): Сессия базы данных для взаимодействия с пользователями.

    Returns:
        UserResponse: Данные о зарегистрированном пользователе.

    Raises:
        HTTPException: В случае, если пользователь с таким email уже существует.
    """
    new_user = await create_user(db, user.username, user.email, user.password)
    return new_user


@router.patch("/me/update/", response_model=UserResponse)
async def update_user_route(
    user_update: UserUpdate,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),  # Добавляем проверку аутентификации
):
    """
    Обновление информации о текущем пользователе.

    Этот маршрут позволяет пользователю обновить своё имя и email. Только аутентифицированные
    пользователи могут обновить свои данные.

    Args:
        user_update (UserUpdate): Данные для обновления (имя пользователя и email).
        db (AsyncSession): Сессия базы данных для взаимодействия с пользователями.
        current_user (dict): Данные о текущем пользователе (получаем из JWT токена).

    Returns:
        UserResponse: Обновленные данные пользователя.

    Raises:
        HTTPException: В случае, если пользователь не найден или данные для обновления некорректны.
    """
    user_id = int(current_user["sub"])

    update_user = await update_user_info(
        db=db,
        user_id=user_id,
        new_username=user_update.username,
        new_email=user_update.email,
    )
    return update_user


@router.get("/me/", response_model=UserResponse)
async def get_user_info_route(
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),  # Добавляем проверку аутентификации
):
    """
    Получение информации о текущем пользователе.

    Этот маршрут возвращает информацию о текущем пользователе, включая имя и email.
    Только аутентифицированные пользователи могут получить доступ к этим данным.

    Args:
        db (AsyncSession): Сессия базы данных для взаимодействия с пользователями.
        current_user (dict): Данные о текущем пользователе (получаем из JWT токена).

    Returns:
        UserResponse: Данные о текущем пользователе.

    Raises:
        HTTPException: В случае, если пользователь не найден.
    """
    user_id = int(current_user["sub"])

    user = await get_user_info(user_id=user_id, db=db)
    return user


@router.delete("/me/delete/", response_model=dict)
async def delete_user_route(
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),  # Добавляем проверку аутентификации
):
    """
    Удаление текущего пользователя.

    Этот маршрут позволяет пользователю удалить свою учетную запись. Только аутентифицированные
    пользователи могут удалить свои данные.

    Args:
        db (AsyncSession): Сессия базы данных для взаимодействия с пользователями.
        current_user (dict): Данные о текущем пользователе (получаем из JWT токена).

    Returns:
        dict: Сообщение об успешном удалении пользователя.

    Raises:
        HTTPException: В случае, если пользователь не найден.
    """
    user_id = int(current_user["sub"])

    return await delete_user(db=db, user_id=user_id)
