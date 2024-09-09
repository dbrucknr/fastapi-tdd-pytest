from typing import AsyncGenerator

import pytest
from aiodocker.containers import DockerContainer

# from database.tests.utils.docker_utils import start_database_container
from database.tests.utils.async_docker import start_testing_database


@pytest.fixture(scope="session", autouse=True)
async def db_session() -> AsyncGenerator[None, None]:
    container: DockerContainer = await start_testing_database()
    print("Container started")
    yield
    await container.stop()
    await container.delete()


# @pytest.fixture(scope="session", autouse=True)
# def db_session():
#     print("Hello World")
#     container = start_database_container()
