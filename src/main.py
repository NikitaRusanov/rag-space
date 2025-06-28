from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from config import settings
from api import router as api_router
from services.vectore_store import get_vectore_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    store = await get_vectore_store()
    await store.client.connect()
    await store.init_collection()
    yield
    await store.client.close()


app = FastAPI(title="rag-space", lifespan=lifespan)

app.include_router(api_router)


@app.get("/is_alive")
async def is_alive():
    return "true"


if __name__ == "__main__":
    uvicorn.run(
        app="main:app", reload=True, host=settings.run.host, port=settings.run.port
    )
