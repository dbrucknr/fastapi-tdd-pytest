from asyncio import get_event_loop_policy
from typing import Generator

import pytest
from aiodocker import Docker, DockerError
from aiodocker.images import DockerImages
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio.engine import AsyncConnection, AsyncEngine
from sqlmodel import SQLModel, create_engine

from database import *
from database.config import DatabaseConfig
from tests.utils.async_docker import start_testing_database

config = DatabaseConfig()
engine = create_engine(
    url=str(config.TEST_SQLALCHEMY_DATABASE_URI), echo=True, future=True
)
async_engine = AsyncEngine(engine)

# https://medium.com/@estretyakov/the-ultimate-async-setup-fastapi-sqlmodel-alembic-pytest-ae5cdcfed3d4


def run_upgrade(connection: AsyncConnection, cfg: Config):
    cfg.config_ini_section = "testdb"
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_session():
    docker = Docker()
    images = DockerImages(docker=docker)
    try:
        await images.pull(from_image="postgres:16.4-alpine3.20")
        container = await start_testing_database(docker)
        await container.start()
        print(f"Container ID: {container.id}")
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        async with async_engine.begin() as connection:
            await connection.run_sync(run_upgrade, Config("alembic.ini"))
    except DockerError as e:
        print(f"Error starting database container: {e}")
    except TimeoutError as e:
        print(e)
    finally:
        # await container.stop()
        # await container.delete()
        await docker.close()
