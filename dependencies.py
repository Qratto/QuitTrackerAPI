from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from database import SessionDep
from core.exceptions import CredentialsException
from models import User
from repositories.habits import BadHabitRepository
from repositories.relapses import RelapseRepository
from repositories.users import UserRepository
from schemas import TokenData
from core.security import SECRET_KEY, ALGORITHM
from services.habits import BadHabitService
from services.relapses import RelapseService
from services.stats import StatsService
from services.users import UserService


# Repositories
def get_habit_repository(session: SessionDep) -> BadHabitRepository:
    return BadHabitRepository(session)


def get_relapse_repository(session: SessionDep) -> RelapseRepository:
    return RelapseRepository(session)


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


HabitRepositoryDep = Annotated[BadHabitRepository, Depends(get_habit_repository)]
RelapseRepositoryDep = Annotated[RelapseRepository, Depends(get_relapse_repository)]
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


# Services
def get_habit_service(repository: HabitRepositoryDep) -> BadHabitService:
    return BadHabitService(repository)


def get_relapse_service(repository: RelapseRepositoryDep) -> RelapseService:
    return RelapseService(repository)


def get_stats_service(
        habit_repository: HabitRepositoryDep,
        relapse_repository: RelapseRepositoryDep) -> StatsService:
    return StatsService(habit_repository, relapse_repository)


async def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)


HabitServiceDep = Annotated[BadHabitService, Depends(get_habit_service)]
RelapseServiceDep = Annotated[RelapseService, Depends(get_relapse_service)]
StatsServiceDep = Annotated[StatsService, Depends(get_stats_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

# Auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], service: UserServiceDep) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise CredentialsException
    user = await service.get_user_by_username(token_data.username)
    if user is None:
        raise CredentialsException
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
