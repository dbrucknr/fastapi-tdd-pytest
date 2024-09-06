from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import declarative_base

from database.config import DatabaseConfig

config = DatabaseConfig()
engine = create_async_engine(
    url=str(config.SQLALCHEMY_DATABASE_URI), echo=True, future=True
)
# session = sessionmaker(bind=True, future=True, autoflush=False, autocommit=False)
base = declarative_base()


async def session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session to perform database operations."""
    try:
        async with AsyncSession(engine) as session:
            yield session
    finally:
        async with AsyncSession(engine) as session:
            await session.close()
