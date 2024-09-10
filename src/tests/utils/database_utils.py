import tracemalloc

from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio.engine import AsyncConnection

tracemalloc.start()


def migrate_to_db(
    connection: AsyncConnection | None = None,
    revision: str = "head",
):
    print(f"Running migration to {revision}")
    config = Config("alembic.ini")
    if connection is not None:
        config.config_ini_section = "testdb"
        config.attributes["connection"] = connection
        command.upgrade(config, revision)
