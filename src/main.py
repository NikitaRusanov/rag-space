from fastapi import FastAPI
import uvicorn

from config import settings
from api import router as api_router

app = FastAPI(title="rag-space")

app.include_router(api_router)


@app.get("/is_alive")
async def is_alive():
    return "true"


if __name__ == "__main__":
    uvicorn.run(
        app="main:app", reload=True, host=settings.run.host, port=settings.run.port
    )
