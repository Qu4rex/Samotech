from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.deps import AuthServiceDep, CurrentUserDep
from src.schemas.token import Token
from src.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, service: AuthServiceDep):
    """Создаёт нового пользователя"""
    
    return await service.register_user(data)


@router.post("/login", response_model=Token)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthServiceDep,):
    """Вход по username и паролю."""

    user = await service.authenticate_user(form.username, form.password)
    return service.create_access_token_for_user(user)


@router.get("/me", response_model=UserRead)
async def read_me(current_user: CurrentUserDep):
    """Возвращает данные пользователя, которому принадлежит токен."""
    
    return current_user