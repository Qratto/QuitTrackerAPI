from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas import UserResponse, UserCreate, Token
from security import create_access_token
from services.users import UserServiceDep

from typing import Annotated

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, service: UserServiceDep):
    return await service.register(user_data)


@auth_router.post("/login", response_model=Token, status_code=200)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: UserServiceDep):
    user = await service.authenticate(form_data.username, form_data.password)
    token = create_access_token({"sub":form_data.username}, None)
    return Token(access_token=token, token_type="bearer")
