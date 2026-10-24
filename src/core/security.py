from datetime import datetime, UTC, timedelta

import jwt
from pwdlib import PasswordHash

from src.core.config import settings

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Хеширует пароль с использованием безопасного алгоритма хеширования."""

    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли пароль хешу."""

    return password_hasher.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Создает JWT токен для пользователя с указанным user_id."""

    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET.get_secret_value(), algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Возвращает id пользователя или None, если токен невалиден или просрочен."""
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET.get_secret_value(), algorithms=[settings.ALGORITHM])
        return int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None