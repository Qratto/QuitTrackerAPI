from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Habit schemas
class BadHabitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None


class CreateBadHabit(BadHabitBase):
    pass


class ResponseBadHabit(BadHabitBase):
    id: int
    started_at: datetime


class BadHabitStats(BaseModel):
    habit_id: int
    name: str
    started_at: datetime
    last_relapse_at: datetime | None
    current_streak_days: int
    longest_streak_days: int
    relapse_count: int


# Relapse schemas
class RelapseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    note: str | None = None


class CreateRelapse(RelapseBase):
    pass


class ResponseRelapse(RelapseBase):
    id: int
    habit_id: int
    occurred_at: datetime
