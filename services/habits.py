from exceptions import HabitNotFound
from models import BadHabit
from repositories.habits import BadHabitRepository
from schemas import CreateBadHabit, EditBadHabit


class BadHabitService:

    def __init__(self, repository: BadHabitRepository):
        self._repository = repository

    async def __get_or_404(self, habit_id: int, user_id: int | None = None) -> BadHabit:
        if user_id is None:
            habit = await self._repository.find_by_id(habit_id)
        else:
            habit = await self._repository.find_by_id_for_user(habit_id, user_id)
        if habit is None:
            raise HabitNotFound(habit_id)
        return habit

    async def get(self, habit_id: int, user_id: int | None = None) -> BadHabit:
        return await self.__get_or_404(habit_id, user_id)

    async def get_all(self, user_id: int | None = None) -> list[BadHabit]:
        if user_id is None:
            return await self._repository.find_all()
        return await self._repository.find_all_by_user(user_id)

    async def create(self, habit_data: CreateBadHabit, user_id: int) -> BadHabit:
        habit = BadHabit(**habit_data.model_dump(), user_id=user_id)
        return await self._repository.save(habit)

    async def update(self, habit_id: int, habit_data: EditBadHabit, user_id: int | None = None) -> BadHabit:
        habit = await self.__get_or_404(habit_id, user_id)
        update_data = habit_data.model_dump(exclude_unset=True)
        if not update_data:
            return habit
        for field, value in update_data.items():
            setattr(habit, field, value)
        return await self._repository.save(habit)

    async def delete(self, habit_id: int, user_id: int | None = None) -> None:
        habit = await self.__get_or_404(habit_id, user_id)
        await self._repository.remove(habit)
