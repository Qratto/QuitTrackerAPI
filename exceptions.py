from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse


class HabitNotFound(Exception):
    def __init__(self, habit_id: int):
        self.habit_id = habit_id


class UsernameExisting(Exception):
    def __init__(self, username: str):
        self.username = username


class UserUnauthorized(Exception):
    def __init__(self):
        pass


class CredentialsException(Exception):
    def __init__(self):
        pass


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HabitNotFound)
    async def habit_not_found_handler(request: Request, exc: HabitNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"Habit with id {exc.habit_id} not found"},
        )

    @app.exception_handler(UsernameExisting)
    async def username_existing_handler(request: Request, exc: UsernameExisting):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": f"Username {exc.username} already exists."}
        )

    @app.exception_handler(UserUnauthorized)
    async def user_unauthorized_handler(request: Request, exc: UserUnauthorized):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )

    @app.exception_handler(CredentialsException)
    async def credentials_exception_handler(request: Request, exc: UserUnauthorized):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Could not validate credentials",
                     "WWW-Authenticate": "Bearer"}
        )
