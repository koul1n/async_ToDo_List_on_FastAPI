from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security.utils import decode_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login/")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        user_data = decode_jwt(token)
        return user_data
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


async def ensure_user_access(user_id: int, current_user: dict = Depends(get_current_user)):

    if int(current_user["sub"]) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this user"
        )