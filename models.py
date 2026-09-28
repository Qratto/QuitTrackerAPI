from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class BadHabit(Base):
    __tablename__ = "bad_habits"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    relapses = relationship("Relapse", back_populates="habit", lazy="selectin")


class Relapse(Base):
    __tablename__ = "relapses"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("bad_habits.id"))
    note = Column(String(200), nullable=True)
    occurred_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    habit = relationship("BadHabit", back_populates="relapses", lazy="selectin")
