from typing import Annotated

from fastapi import Depends

from models import BadHabit
from repositories.habits import BadHabitRepository, HabitRepositoryDep
from schemas import CreateBadHabit, EditBadHabit


class BadHabitService:

    def __init__(self, repository: BadHabitRepository):
        self._repository = repository

    async def get(self, habit_id: int):
        habit = await self._repository.find_by_id(habit_id)
        return habit

    async def get_all(self):
        habits = await self._repository.find_all()
        return habits

    async def create(self, habit_data: CreateBadHabit):
        habit = BadHabit(**habit_data.model_dump())
        return await self._repository.save(habit)

    async def update(self, habit_id: int, habit_data: EditBadHabit):
        habit_db = await self._repository.find_by_id(habit_id)
        if habit_db is None:
            return None
        update_data = habit_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(habit_db, field, value)

        return await self._repository.save(habit_db)

    async def delete(self, habit_id: int):
        habit = await self._repository.find_by_id(habit_id)
        await self._repository.remove(habit)


def get_habit_service(repository: HabitRepositoryDep) -> BadHabitService:
    return BadHabitService(repository)


HabitServiceDep = Annotated[BadHabitService, Depends(get_habit_service)]
