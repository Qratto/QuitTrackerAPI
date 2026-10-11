from fastapi import APIRouter

from dependencies import CurrentUserDep, UserServiceDep
from core.exceptions import UserForbidden
from schemas import UserResponse

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("", response_model=list[UserResponse], status_code=200)
async def show_users(service: UserServiceDep, user: CurrentUserDep):
    if not user.is_admin:
        raise UserForbidden
    return await service.get_all()


@user_router.get("/{user_id}", response_model=UserResponse, status_code=200)
async def show_user(user_id: int, service: UserServiceDep, user: CurrentUserDep):
    if not user.is_admin:
        raise UserForbidden
    return await service.get(user_id)
