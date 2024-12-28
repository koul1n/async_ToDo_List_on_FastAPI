from fastapi import APIRouter, Depends
from app.users import (
    UserResponse,
    UserCreate,
    create_user,
    update_user_info,
    UserUpdate,
    get_user_info,
    delete_user,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import database_helper


router = APIRouter(prefix="/users")


@router.post("/", response_model=UserResponse)
async def create_user_route(
    user: UserCreate, db: AsyncSession = Depends(database_helper.get_db)
):
    new_user = await create_user(db, user.username, user.email, user.password)
    return new_user


@router.patch("/update/", response_model=UserResponse)
async def update_user_route(
    user_update: UserUpdate, db: AsyncSession = Depends(database_helper.get_db)
):
    update_user = await update_user_info(
        db=db,
        user_id=user_update.id,
        new_username=user_update.username,
        new_email=user_update.email,
    )
    return update_user


@router.get("/{user_id}/", response_model=UserResponse)
async def get_user_info_route(
    user_id: int, db: AsyncSession = Depends(database_helper.get_db)
):
    user = await get_user_info(user_id=user_id, db=db)
    return user


@router.delete("/{user_id}/", response_model=dict)
async def delete_user_route(
    user_id: int, db: AsyncSession = Depends(database_helper.get_db)
):
    return await delete_user(db=db, user_id=user_id)
