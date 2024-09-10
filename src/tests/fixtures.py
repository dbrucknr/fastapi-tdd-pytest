from asyncio import get_event_loop_policy
from typing import AsyncGenerator, Generator

import pytest
from aiodocker import Docker, DockerError
from aiodocker.images import DockerImages
from alembic import command
from alembic.config import Config
from pytest import FixtureRequest
from sqlalchemy.ext.asyncio.engine import AsyncConnection, AsyncEngine
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from database import *
from database.config import DatabaseConfig

config = DatabaseConfig()
engine = create_engine(
    url=str(config.TEST_SQLALCHEMY_DATABASE_URI), echo=True, future=True
)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", config.TEST_SQLALCHEMY_DATABASE_URI)
async_engine = AsyncEngine(engine)

# https://medium.com/@estretyakov/the-ultimate-async-setup-fastapi-sqlmodel-alembic-pytest-ae5cdcfed3d4


def run_upgrade(connection: AsyncConnection, cfg: Config):
    cfg.config_ini_section = "testdb"
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


@pytest.fixture(scope="session")
def event_loop(request: FixtureRequest) -> Generator:  # noqa: indirect usage
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def create_testing_database():
    docker = Docker()
    images = DockerImages(docker=docker)
    try:
        await images.pull(from_image="postgres:16.4-alpine3.20")
        container = await docker.containers.create_or_replace(
            name="test-db",
            config={
                "Image": "postgres:16.4-alpine3.20",
                "Env": [
                    "POSTGRES_USER=postgres",
                    "POSTGRES_PASSWORD=postgres",
                    "POSTGRES_DB=postgres",
                ],
                # "ExposedPorts": {"5432/tcp": {}},
                "HostConfig": {
                    "PortBindings": {"5432/tcp": [{"HostPort": "5434"}]},
                },
            },
        )
        await container.start()
        for container in await docker.containers.list():
            print(f" {container._id}")
        return container
    except DockerError as e:
        print(f"Failed to start the database container: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await container.stop()
        await container.delete(force=True)
        await docker.close()


@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


# Note: This appears to run into an error where the migration adds columns that already exist
# @pytest.fixture(scope="session", autouse=True)
# async def migrate():
#     async with async_engine.begin() as connection:
#         await connection.run_sync(run_upgrade, Config("alembic.ini"))


@pytest.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session
        await session.close()
        await async_engine.dispose()


@pytest.fixture(scope="session")
async def db_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.connect() as connection:
        yield connection
        await connection.close()
        await async_engine.dispose()
