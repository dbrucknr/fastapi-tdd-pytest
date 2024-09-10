from fastapi import Depends, FastAPI

from api.lifespan import lifespan
from database.config import DatabaseConfig, get_db_config
from database.connect import AsyncSession, session

api = FastAPI(lifespan=lifespan)


@api.get(path="/")
async def index(
    database: AsyncSession = Depends(session),
    config: DatabaseConfig = Depends(get_db_config),
) -> dict:
    return {"configuration": await config}
