from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator, Annotated

engine = create_async_engine(settings.database_url)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


SessionDep = Annotated[AsyncSession, Depends(get_session)]
