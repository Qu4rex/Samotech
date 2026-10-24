from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Базовая модель пользователя."""
    
    email: EmailStr
    username: str = Field(min_length=3, max_length=32)


class UserCreate(UserBase):
    """Тело запроса на регистрацию."""

    password: str = Field(min_length=8, max_length=128)


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    """Модель пользователя для ответа API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime