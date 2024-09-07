import pytest

from database.tests.utils.docker_utils import start_database_container


@pytest.fixture(scope="session", autouse=True)
def db_session():
    container = start_database_container()
