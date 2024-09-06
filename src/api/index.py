from fastapi import Depends, FastAPI

from api.lifespan import lifespan
from database.connect import AsyncSession, session

api = FastAPI(lifespan=lifespan)


@api.get(path="/")
async def index(database: AsyncSession = Depends(session)) -> dict:
    return {"message": "Hello, World!"}
