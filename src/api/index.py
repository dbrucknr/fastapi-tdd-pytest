from fastapi import FastAPI

api = FastAPI()


@api.get(path="/")
async def index() -> dict:
    return {"message": "Hello, World!"}
