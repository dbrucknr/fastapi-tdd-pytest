from typing import AsyncGenerator

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from database.config import DatabaseConfig

config = DatabaseConfig()
engine = create_engine(url=str(config.SQLALCHEMY_DATABASE_URI), echo=True, future=True)
async_engine = AsyncEngine(engine)


async def session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session to perform database operations."""
    try:
        async with AsyncSession(async_engine) as session:
            yield session
    finally:
        async with AsyncSession(async_engine) as session:
            await session.close()


async def create_all_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
