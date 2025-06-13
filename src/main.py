from fastapi import FastAPI
import uvicorn


app = FastAPI(title="rag-space")


@app.get("/is_alive")
async def is_alive():
    return "true"


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
