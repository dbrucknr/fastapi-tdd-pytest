from fastapi import FastAPI

api = FastAPI()

@api.get(path="/")
async def index():
    return {"message": "Hello, World!"}