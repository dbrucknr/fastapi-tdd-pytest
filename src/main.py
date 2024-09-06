from uvicorn import run

if __name__ == "__main__":
    run(app="api.index:api", reload=True)