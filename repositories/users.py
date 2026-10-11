from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_username(self, username: str) -> User:
        result = await self._session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def save(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def find_all(self) -> list[User]:
        result = await self._session.execute(select(User))
        return list(result.scalars().all())

    async def find_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)