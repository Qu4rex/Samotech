from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import InvalidTokenError
from src.core.security import decode_access_token
from src.crud.user import UserCRUD
from src.db.session import get_async_session
from src.models.user import User
from src.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_user_crud(session: SessionDep) -> UserCRUD:
    """Создаёт UserCRUD на сессии текущего запроса"""
    return UserCRUD(session)

UserCRUDDep = Annotated[UserCRUD, Depends(get_user_crud)]


def get_auth_service(session: SessionDep, users: UserCRUDDep) -> AuthService:
    """Создаёт AuthService. Сессия общая с UserCRUD: FastAPI кэширует зависимости в рамках запроса"""
    return AuthService(session, users)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], users: UserCRUDDep,) -> User:
    """Возвращает пользователя по Bearer-токену"""
    
    user_id = decode_access_token(token)
    if user_id is None:
        raise InvalidTokenError()
    user = await users.get_by_id(user_id)
    if user is None or not user.is_active:
        raise InvalidTokenError()
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]