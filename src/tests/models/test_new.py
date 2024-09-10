import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_condition_is_true(db_session):
    assert True
