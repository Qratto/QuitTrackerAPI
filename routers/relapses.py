from fastapi import APIRouter
from schemas import ResponseRelapse, CreateRelapse
from dependencies import RelapseServiceDep

relapse_router = APIRouter(tags=["relapses"])


@relapse_router.post("/habits/{habit_id}/relapses", response_model=ResponseRelapse, status_code=201)
async def mark_relapse(habit_id: int, relapse_data: CreateRelapse, service: RelapseServiceDep):
    return await service.create(habit_id, relapse_data)


@relapse_router.get("/habits/{habit_id}/relapses", response_model=list[ResponseRelapse], status_code=200)
async def show_relapses(habit_id: int, service: RelapseServiceDep):
    return await service.get_all_by_habit(habit_id)
