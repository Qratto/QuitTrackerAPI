from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse


class HabitNotFound(Exception):
    def __init__(self, habit_id: int):
        self.habit_id = habit_id


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HabitNotFound)
    async def habit_not_found_handler(request: Request, exc: HabitNotFound):
        return JSONResponse(
            status_code=404,
            content={"message": f"Habit with id {exc.habit_id} not found"},
        )
