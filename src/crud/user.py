from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class UserCRUD():
    """Класс для выполнения операций CRUD (создание, чтение, обновление, удаление) с пользователями в базе данных."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def get_by_id(self, user_id: int) -> User | None:
        """Получить пользователя по id."""

        return await self.session.get(User, user_id)

    
    async def get_by_email(self, email: str) -> User | None:
        """Получить пользователя по email."""

        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()


    async def get_by_username(self, username: str) -> User | None:
        """Получить пользователя по username."""

        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()


    async def create(self, *, email: str, username: str, hashed_password: str, ) -> User:
        """Создать нового пользователя в базе данных."""

        new_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )
        self.session.add(new_user)
        await self.session.flush()
        await self.session.refresh(new_user)
        return new_user