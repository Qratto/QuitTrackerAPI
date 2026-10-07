from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)


class BadHabit(Base):
    __tablename__ = "bad_habits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    relapses = relationship("Relapse", back_populates="habit", lazy="selectin", cascade="all, delete-orphan")
    owner = relationship("User")


class Relapse(Base):
    __tablename__ = "relapses"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("bad_habits.id"), nullable=False)
    note = Column(String(200), nullable=True)
    occurred_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    habit = relationship("BadHabit", back_populates="relapses", lazy="selectin")
