from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from database import SessionDep
from models import Relapse


class RelapseRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_habit(self, habit_id: int) -> list[Relapse]:
        result = await self._session.execute(select(Relapse).where(Relapse.habit_id == habit_id))
        return list(result.scalars().all())

    async def save(self, relapse: Relapse) -> Relapse:
        self._session.add(relapse)
        await self._session.commit()
        await self._session.refresh(relapse)
        return relapse


def get_relapse_repository(session: SessionDep) -> RelapseRepository:
    return RelapseRepository(session)


RelapseRepositoryDep = Annotated[RelapseRepository, Depends(get_relapse_repository)]
