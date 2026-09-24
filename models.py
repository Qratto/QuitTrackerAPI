from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class BadHabit(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    description: Optional[str] = None
    started_at: datetime = Field(default_factory=utcnow)
    created_at: datetime = Field(default_factory=utcnow)

    relapses: List["Relapse"] = Relationship(back_populates="habit")

class Relapse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="badhabit.id")
    occurred_at: datetime = Field(default_factory=utcnow)
    note: Optional[str] = None

    habit: Optional[BadHabit] = Relationship(back_populates="relapses")