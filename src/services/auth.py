from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import create_access_token, hash_password, verify_password
from src.crud.user import UserCRUD
from src.models.user import User
from src.schemas.token import Token
from src.schemas.user import UserCreate
from src.core.exceptions import (
    EmailTakenError, InactiveUserError, InvalidCredentialsError,
    UserAlreadyExistsError, UsernameTakenError,
)


_DUMMY_HASHED_PASSWORD = hash_password("dummy-password")


class AuthService:
    """Сервис для аутентификации пользователей."""

    def __init__(self, session: AsyncSession, users: UserCRUD) -> None:
        self.session = session
        self.users = users


    async def register_user(self, data: UserCreate) -> User:    
        """Регистрирует нового пользователя в системе."""

        email = data.email.lower()

        if await self.users.get_by_email(email):
            raise EmailTakenError
        if await self.users.get_by_username(data.username):
            raise UsernameTakenError

        try:
            user = await self.users.create(
                email=email,
                username=data.username,
                hashed_password=hash_password(data.password),
            )
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExistsError

        return user


    async def authenticate_user(self, username: str, password: str) -> User:
        """Аутентифицирует пользователя по username и паролю."""

        user = await self.users.get_by_username(username)

        if not user:
            verify_password(password, _DUMMY_HASHED_PASSWORD)
            raise InvalidCredentialsError

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError

        if not user.is_active:
            raise InactiveUserError

        return user


    async def create_access_token_for_user(self, user: User) -> Token:
        """Создает JWT токен для аутентифицированного пользователя."""

        access_token = create_access_token(user_id=user.id)
        return Token(access_token=access_token, token_type="bearer")