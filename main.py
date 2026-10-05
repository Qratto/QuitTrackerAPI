from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import engine, Base

from exceptions import register_exception_handlers
from routers.habits import habit_router
from routers.relapses import relapse_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(habit_router)
app.include_router(relapse_router)


@app.get("/health", status_code=200)
async def check_work():
    return {"status": "ok"}
