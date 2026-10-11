from models import Relapse
from schemas import CreateRelapse
from repositories.relapses import RelapseRepository
from repositories.habits import BadHabitRepository
from core.exceptions import HabitNotFound


class RelapseService:
    def __init__(self, habit_repository: BadHabitRepository, relapse_repository: RelapseRepository):
        self._habit_repository = habit_repository
        self._relapse_repository = relapse_repository

    async def __belongs_or_404(self, habit_id: int, user_id: int) -> None:
        habit = await self._habit_repository.find_by_id_for_user(habit_id, user_id)
        if habit is None:
            raise HabitNotFound(habit_id)

    async def get_all_by_habit(self, habit_id: int, user_id: int) -> list[Relapse]:
        await self.__belongs_or_404(habit_id, user_id)
        return await self._relapse_repository.find_by_habit(habit_id)

    async def create(self, habit_id: int, user_id: int, relapse_data: CreateRelapse) -> Relapse:
        await self.__belongs_or_404(habit_id, user_id)
        relapse = Relapse(**relapse_data.model_dump(), habit_id=habit_id)
        return await self._relapse_repository.save(relapse)
