import pytest
from sqlmodel import inspect


@pytest.mark.asyncio(loop_scope="session")
async def test_model_structure_table_exists(db_connection):
    def sync_inspect(connection):
        inspector = inspect(connection)
        return inspector.get_table_names()

    table_names = await db_connection.run_sync(sync_inspect)
    assert "category" in table_names
