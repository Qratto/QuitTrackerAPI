from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from database import SessionDep, engine, Base
from models import BadHabit, Relapse
from schemas import ResponseBadHabit, CreateBadHabit, CreateRelapse, ResponseRelapse, BadHabitStats, EditBadHabit

from datetime import datetime, timezone, timedelta


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health", status_code=200)
async def check_work():
    return {"status": "ok"}


@app.get("/habit", response_model=list[ResponseBadHabit], status_code=200)
async def show_habits(session: SessionDep):
    result = await session.execute(select(BadHabit))
    return result.scalars().all()


@app.get("/habit/{habit_id}", response_model=ResponseBadHabit, status_code=200)
async def show_habit(habit_id: int, session: SessionDep):
    habit = await session.get(BadHabit, habit_id)
    return habit


@app.delete("/habit/{habit_id}", status_code=200)
async def delete_habit(habit_id: int, session: SessionDep):
    habit = await session.get(BadHabit, habit_id)
    await session.delete(habit)
    await session.commit()
    return {"ok": True}


@app.patch("/habit/{habit_id}", response_model=ResponseBadHabit, status_code=200)
async def update_habit(habit_id: int, habit_data: EditBadHabit, session: SessionDep):
    habit_db = await session.get(BadHabit, habit_id)
    if not habit_db:
        raise HTTPException(status_code=404, detail="Not found")
    update_data = habit_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(habit_db, field, value)

    await session.commit()
    await session.refresh(habit_db)
    return habit_db


@app.post("/habit", response_model=ResponseBadHabit, status_code=201)
async def create_habit(habit_data: CreateBadHabit, session: SessionDep):
    habit = BadHabit(**habit_data.model_dump())
    session.add(habit)
    await session.commit()
    await session.refresh(habit)
    return habit


@app.post("/habit/{habit_id}/relapses", response_model=ResponseRelapse, status_code=201)
async def mark_relapse(habit_id: int, relapse_data: CreateRelapse, session: SessionDep):
    habit = await session.get(BadHabit, habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Not found")
    relapse = Relapse(**relapse_data.model_dump(), habit_id=habit_id)
    session.add(relapse)
    await session.commit()
    await session.refresh(relapse)
    return relapse


@app.get("/habit/{habit_id}/relapses", response_model=list[ResponseRelapse], status_code=200)
async def show_relapses(habit_id: int, session: SessionDep):
    result = await session.execute(select(Relapse).where(Relapse.habit_id == habit_id))
    return result.scalars().all()


@app.get("/habit/{habit_id}/stats", response_model=BadHabitStats, status_code=200)
async def get_stats(habit_id: int, session: SessionDep):
    habit = await session.get(BadHabit, habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Not found")
    result = await session.execute(select(Relapse).where(Relapse.habit_id == habit_id))
    relapses = result.scalars().all()
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

    return BadHabitStats(habit_id=habit_id,
                         name=habit.name,
                         started_at=habit.started_at,
                         last_relapse_at=last_relapse,
                         current_streak_days=current_streak.days,
                         longest_streak_days=longest_streak.days,
                         relapse_count=len(relapses)
                         )
