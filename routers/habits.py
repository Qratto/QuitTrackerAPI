from fastapi import APIRouter

from schemas import ResponseBadHabit, EditBadHabit, BadHabitStats, CreateBadHabit
from dependencies import HabitServiceDep
from dependencies import StatsServiceDep

habit_router = APIRouter(prefix="/habits", tags=["habits"])


@habit_router.get("/", response_model=list[ResponseBadHabit], status_code=200)
async def show_habits(service: HabitServiceDep):
    return await service.get_all()


@habit_router.get("/{habit_id}", response_model=ResponseBadHabit, status_code=200)
async def show_habit(habit_id: int, service: HabitServiceDep):
    return await service.get(habit_id)


@habit_router.post("/", response_model=ResponseBadHabit, status_code=201)
async def create_habit(habit_data: CreateBadHabit, service: HabitServiceDep):
    return await service.create(habit_data)


@habit_router.patch("/{habit_id}", response_model=ResponseBadHabit, status_code=200)
async def update_habit(habit_id: int, habit_data: EditBadHabit, service: HabitServiceDep):
    return await service.update(habit_id, habit_data)


@habit_router.delete("/{habit_id}", status_code=204)
async def delete_habit(habit_id: int, service: HabitServiceDep):
    await service.delete(habit_id)
    return None


@habit_router.get("/{habit_id}/stats", response_model=BadHabitStats, status_code=200)
async def get_stats(habit_id: int, service: StatsServiceDep):
    return await service.get(habit_id)
