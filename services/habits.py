from exceptions import HabitNotFound
from models import BadHabit
from repositories.habits import BadHabitRepository
from schemas import CreateBadHabit, EditBadHabit


class BadHabitService:

    def __init__(self, repository: BadHabitRepository):
        self._repository = repository

    async def __get_or_404(self, habit_id: int) -> BadHabit:
        habit = await self._repository.find_by_id(habit_id)
        if habit is None:
            raise HabitNotFound(habit_id)
        return habit

    async def get(self, habit_id: int) -> BadHabit:
        return await self.__get_or_404(habit_id)

    async def get_all(self) -> list[BadHabit]:
        return await self._repository.find_all()

    async def create(self, habit_data: CreateBadHabit) -> BadHabit:
        habit = BadHabit(**habit_data.model_dump())
        return await self._repository.save(habit)

    async def update(self, habit_id: int, habit_data: EditBadHabit) -> BadHabit:
        habit = await self.__get_or_404(habit_id)
        update_data = habit_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(habit, field, value)
        return await self._repository.save(habit)

    async def delete(self, habit_id: int) -> None:
        habit = await self.__get_or_404(habit_id)
        await self._repository.remove(habit)
