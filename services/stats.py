from datetime import timedelta, timezone, datetime
from models import Relapse, BadHabit
from repositories.habits import BadHabitRepository
from repositories.relapses import RelapseRepository
from schemas import BadHabitStats


class StatsService:
    def __init__(self, habit_repository: BadHabitRepository, relapse_repository: RelapseRepository):
        self._habit_repository = habit_repository
        self._relapse_repository = relapse_repository

    @staticmethod
    async def __calculate_stats(habit: BadHabit, relapses: list[Relapse]):
        now = datetime.now(timezone.utc)
        started_at = habit.started_at.replace(tzinfo=timezone.utc)

        if not relapses:
            last_relapse = None
            current_streak = now - started_at
            longest_streak = current_streak
        else:
            occurred_dates = []
            for i in range(len(relapses)):
                occurred_dates.append(relapses[i].occurred_at)
            last_relapse = max(occurred_dates)
            current_streak = now - last_relapse.replace(tzinfo=timezone.utc)
            occurred_dates.sort()
            longest_streak = timedelta(0)
            started_streak = occurred_dates[0].replace(tzinfo=timezone.utc) - started_at
            for i in range(len(occurred_dates) - 1):
                delta_occurred = occurred_dates[i + 1] - occurred_dates[i]
                longest_streak = max(started_streak, delta_occurred)
            longest_streak = max(longest_streak, current_streak)

        return BadHabitStats(habit_id=habit.id,
                             name=habit.name,
                             started_at=habit.started_at,
                             last_relapse_at=last_relapse,
                             current_streak_days=current_streak.days,
                             longest_streak_days=longest_streak.days,
                             relapse_count=len(relapses)
                             )

    async def get(self, habit_id: int):
        habit = await self._habit_repository.find_by_id(habit_id)
        relapses = await self._relapse_repository.find_by_habit(habit_id)
        return await self.__calculate_stats(habit, relapses)
