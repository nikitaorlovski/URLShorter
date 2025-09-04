import uvicorn
from fastapi import FastAPI
from database.database import create_tables
from routers.urls import router as url_router
from routers.redirects import router as redirect_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("Created Tables")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(url_router)
app.include_router(redirect_router)

if __name__ == "__main__":
    uvicorn.run("main:app",host= "127.0.0.1", port=8000, reload=True)

