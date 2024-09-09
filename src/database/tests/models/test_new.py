from asyncio import sleep

import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_condition_is_true():
    await sleep(2)
    assert True
