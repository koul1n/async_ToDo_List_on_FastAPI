import bcrypt
from app.security.config import auth_settings
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status


def hash_password(pwd: str) -> str:
    hashed_bytes = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")  # Преобразование байтов в строку


def validate_password(pwd: str, hashed_pwd: str) -> bool:
    return bcrypt.checkpw(password=pwd.encode(), hashed_password=hashed_pwd.encode())


def create_jwt(
    data: dict,
    key: str = auth_settings.SECRET_KEY,
    algorithm: str = auth_settings.ALGORITHM,
) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=auth_settings.expires_in
    )
    data["sub"] = str(data["sub"])
    payload = {**data, "exp": expiration_time}
    return jwt.encode(payload, key, algorithm=algorithm)


def decode_jwt(
    token: str,
    key: str = auth_settings.SECRET_KEY,
    algorithm: str = auth_settings.ALGORITHM,
) -> dict:
    try:
        decoded_token = jwt.decode(token, key, algorithms=[algorithm])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
