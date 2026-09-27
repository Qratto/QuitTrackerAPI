from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator, Annotated

URL = "sqlite+aiosqlite:///./tracker.db"

engine = create_async_engine(URL, echo=False)

async_session = async_sessionmaker(engine, class_=AsyncSession,expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


SessionDep = Annotated[AsyncSession, Depends(get_session)]
