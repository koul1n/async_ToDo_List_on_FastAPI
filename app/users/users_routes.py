from fastapi import APIRouter, Depends
from app.users import UserResponse, UserCreate, create_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db


router = APIRouter(prefix='/users')



@router.post("/", response_model=UserResponse)
async def create_user_route(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(db, user.username, user.email, user.password)
    return new_user