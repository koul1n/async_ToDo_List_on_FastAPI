from fastapi import APIRouter, Depends, HTTPException, status
from app.users import (
    UserResponse,
    UserCreate,
    create_user,
    update_user_info,
    UserUpdate,
    get_user_info,
    delete_user,
    get_user_by_email
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import database_helper
from app.security import get_current_user, validate_password, create_jwt, TokenInfo, ensure_user_access
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users")


@router.post("/login/", response_model=TokenInfo)
async def login_route(form_data: OAuth2PasswordRequestForm = Depends(),
                      db: AsyncSession = Depends(database_helper.get_db)):
    # Получаем пользователя из базы данных по email
    user = await get_user_by_email(db=db, email=form_data.username)

    # Проверяем пароль пользователя
    if user and validate_password(pwd=form_data.password, hashed_pwd=user.password):
        # Генерируем JWT токен
        token = create_jwt({"sub": user.id, "username": user.username})
        return TokenInfo(access_token=token, token_type="Bearer")

    # Если данные неверные, генерируем ошибку
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )


@router.post("/", response_model=UserResponse)
async def create_user_route(
    user: UserCreate, db: AsyncSession = Depends(database_helper.get_db)
):
    new_user = await create_user(db, user.username, user.email, user.password)
    return new_user


@router.patch("/update/", response_model=UserResponse)
async def update_user_route(
    user_update: UserUpdate,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user)  # Добавляем проверку аутентификации
):
    await ensure_user_access(user_update.id, current_user)

    update_user = await update_user_info(
        db=db,
        user_id=user_update.id,
        new_username=user_update.username,
        new_email=user_update.email,
    )
    return update_user


@router.get("/{user_id}/", response_model=UserResponse)
async def get_user_info_route(
    user_id: int,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user)  # Добавляем проверку аутентификации
):
    await ensure_user_access(user_id, current_user)

    user = await get_user_info(user_id=user_id, db=db)
    return user


@router.delete("/{user_id}/", response_model=dict)
async def delete_user_route(
    user_id: int,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user)  # Добавляем проверку аутентификации
):
    await ensure_user_access(user_id, current_user)

    return await delete_user(db=db, user_id=user_id)
