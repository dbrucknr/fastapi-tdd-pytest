from fastapi import Depends, FastAPI

from database.connect import AsyncSession, session

api = FastAPI()


@api.get(path="/")
async def index(database: AsyncSession = Depends(session)) -> dict:
    return {"message": "Hello, World!"}
