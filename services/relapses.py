from typing import Annotated
from fastapi import Depends

from models import Relapse
from schemas import CreateRelapse

from repositories.relapses import RelapseRepository, RelapseRepositoryDep


class RelapseService:
    def __init__(self, repository: RelapseRepository):
        self._repository = repository

    async def get_all_by_habit(self, habit_id: int):
        return await self._repository.find_by_habit(habit_id)

    async def create(self, habit_id: int, relapse_data: CreateRelapse):
        relapse = Relapse(**relapse_data.model_dump(), habit_id=habit_id)
        return await self._repository.save(relapse)


def get_relapse_service(repository: RelapseRepositoryDep) -> RelapseService:
    return RelapseService(repository)


RelapseServiceDep = Annotated[RelapseService, Depends(get_relapse_service)]
