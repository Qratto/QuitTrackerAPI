from fastapi import APIRouter
from schemas import ResponseRelapse, CreateRelapse
from dependencies import RelapseServiceDep, CurrentUserDep

relapse_router = APIRouter(tags=["relapses"])


@relapse_router.post("/habits/{habit_id}/relapses", response_model=ResponseRelapse, status_code=201)
async def mark_relapse(habit_id: int, relapse_data: CreateRelapse, service: RelapseServiceDep, user: CurrentUserDep):
    return await service.create(habit_id, user.id, relapse_data)


@relapse_router.get("/habits/{habit_id}/relapses", response_model=list[ResponseRelapse], status_code=200)
async def show_relapses(habit_id: int, service: RelapseServiceDep, user: CurrentUserDep):
    return await service.get_all_by_habit(habit_id, user.id)
