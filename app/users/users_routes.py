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
    get_user,
    get_user_info,
    update_user_info,
)

router = APIRouter(prefix="/api/v1/users")


@router.post("/login/", response_model=TokenInfo)
async def login_route(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database_helper.get_db),
):
    user = await get_user(db=db, email=form_data.username)

    if user and validate_password(pwd=form_data.password, hashed_pwd=user.password):
        token = create_jwt({"sub": str(user.id), "username": user.username})
        return TokenInfo(access_token=token, token_type="Bearer")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )


@router.post("/register/", response_model=UserResponse)
async def create_user_route(
    user: UserCreate, db: AsyncSession = Depends(database_helper.get_db)
):

    new_user = await create_user(
        db=db, username=user.username, email=user.email, password=user.password
    )
    return new_user


@router.patch("/me/update/", response_model=UserResponse)
async def update_user_route(
    user_update: UserUpdate,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):

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
    current_user: dict = Depends(get_current_user),
):

    user_id = int(current_user["sub"])

    user = await get_user_info(db=db, user_id=user_id)
    return user


@router.delete("/me/delete/", response_model=dict)
async def delete_user_route(
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])

    return await delete_user(db=db, user_id=user_id)
