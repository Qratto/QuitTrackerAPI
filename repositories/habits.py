from sqlalchemy.ext.asyncio import AsyncSession
from models import BadHabit
from sqlalchemy import select


class BadHabitRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, habit_id: int) -> BadHabit | None:
        return await self._session.get(BadHabit, habit_id)

    async def find_all(self) -> list[BadHabit]:
        result = await self._session.execute(select(BadHabit))
        return list(result.scalars().all())

    async def save(self, habit: BadHabit) -> BadHabit:
        self._session.add(habit)
        await self._session.commit()
        await self._session.refresh(habit)
        return habit

    async def remove(self, habit: BadHabit) -> None:
        await self._session.delete(habit)
        await self._session.commit()
