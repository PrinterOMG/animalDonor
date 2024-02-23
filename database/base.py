from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import sqlalchemy as sa

from settings import settings

postgres_dsn = f'postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@postgres:5432/{settings.postgres_db}'
engine = create_async_engine(postgres_dsn)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
